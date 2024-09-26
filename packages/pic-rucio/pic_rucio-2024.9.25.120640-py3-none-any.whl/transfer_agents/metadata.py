# import modules
from __future__ import annotations

import copy
import hashlib
import json
import linecache
import logging
import os
import re
import sys
import unittest
import uuid
from string import Template

import yaml

from transfer_agents.config import get_config_file
from transfer_agents.config import RucioClientConfig
from transfer_agents.db_functions import dbData
from transfer_agents.transfer_file import TransferFile

# import Classes

DEFAULT_DIR = "/"


class MetaData:
    def __init__(
        self,
        config: RucioClientConfig,
        csv_file: str = None,
    ):

        self.config = config
        self.logger = logging.getLogger("metadata")

        # import functions from db_functions.py
        self.db = dbData(config)
        self.transfer_file = None
        if csv_file:
            self.transfer_file = TransferFile(config, csv_file)

    def list_files(self):
        """Get the list of files to transfer
        from the convenient source"""
        if self.transfer_file:
            return self.list_files_csv()
        else:
            return self.list_files_db()

    def get_file_for_project(self, file, project_name):
        """Fill the file dict for a specific project

        Arguments:
            file: dict, should contain at least the "name"
            project_name: subsections in "Data Types"
        """
        file_name = file["name"]
        metadata = self.datatype_metadata(project_name, file_name)
        if metadata is None:
            return None

        # Source pfn
        source_dir = self.datatype_sourcepfn(project_name, file_name)
        file["sourcepfn"] = Template(source_dir).safe_substitute(
            metadata,
        )
        self.logger.debug(f"Source pfn: {file['sourcepfn']}")

        # Dest pfn
        dest_dir = self.datatype_destpfn(project_name, file_name)
        output_path = self.config.datatype_output_path(project_name)
        if output_path is None:
            file["destpfn"] = Template(dest_dir).safe_substitute(
                metadata,
            )
        else:
            file["destpfn"] = list(
                self.db.execute_query(output_path.format(file_name)),
            )[0]
        self.logger.debug(f"Dest pfn: {file['destpfn']}")

        file["collection"] = self.config.datatype_rule(
            project_name,
        )
        file["metadata"] = self.parse_metadata(
            project_name,
            metadata,
        )

        # Dataset / Container organization
        file["organization"] = self.parse_organization(
            project_name,
            metadata,
        )
        self.logger.debug(f"Organization: {file['organization']}")

        file["priority"] = self.config.datatype_priority(
            project_name,
        )

        return file

    def list_files_db(self):
        project_list = self.config.datatype_list
        self.logger.debug(f"Identified these sections : {project_list}")

        list_metadata = list()

        for project_name in project_list:
            self.logger.info(f"Listing files for project: {project_name}")
            if not self.config.datatype_transfer(project_name) is True:
                self.logger.info(f"Project {project_name} is disabled, skipping it")
                continue

            # Query the files to transfer
            query = Template(self.config.datatype_query(project_name)).safe_substitute(
                dict(self.config.datatype_regex(project_name).items()),
            )
            self.logger.debug(f"Query: {query}")
            file_list = self.db.execute_query(query)

            if len(file_list) == 0:
                self.logger.info("No files to transfer in project: {project_name}")
                continue
            else:
                self.logger.debug(f"Found these files to process {file_list}")

            # Iterate over the list of files to get their metadata
            for file_name in file_list:
                file = self.get_file_for_project({"name": file_name}, project_name)
                if file:
                    list_metadata.append(file)
        return list_metadata

    def list_files_csv(self):
        project_list = self.config.datatype_list
        self.logger.info(project_list)
        list_files = self.transfer_file.get_csv_data()
        list_metadata = list()
        if len(list_files) == 0:
            self.logger.info("No files to transfer")
            return list_metadata

        for project_name in project_list:
            self.logger.info(f"Processing project: {project_name}")
            if self.config.datatype_transfer(project_name) == True:
                for index, row in list_files.iterrows():
                    file = {
                        "name": row[0],
                        "checksum": row[1],
                        "size": row[2],
                    }
                    file = self.get_file_for_project(file, project_name)
                    if file:
                        list_metadata.append(file)
        return list_metadata

    def datatype_sourcepfn(self, data_type, file_name):

        source_dir = self.config.datatype_sourcedir(data_type)
        if not source_dir:
            source_dir = self.get_deterministic_folder(file_name)

        return os.path.join(
            self.config.datatype_basedir(data_type),
            source_dir,
            file_name,
        )

    def datatype_destpfn(self, data_type, file_name):
        if file_name.startswith("/"):
            file_name = file_name[1:]
        dest_dir = self.config.datatype_destdir(data_type)
        if not dest_dir:
            dest_dir = self.get_deterministic_folder(file_name)

        return os.path.join(
            self.config.datatype_basedir(data_type),
            dest_dir,
            file_name,
        )

    def replace_metadata_in_section(self, metadata, section):
        self.logger.debug(f"Replacing metadata {metadata} in section {section}")
        new_section = copy.deepcopy(section)
        for k, v in new_section.items():
            new_section[k] = Template(v).safe_substitute(metadata)
        self.logger.debug(f"Replacement result {new_section}")
        return new_section

    def parse_organization(self, data_type, metadata):
        template = self.config.datatype_organization(data_type)
        return self.replace_metadata_in_section(metadata, template)

    def parse_metadata(self, data_type, metadata):
        template = self.config.datatype_metadata(data_type)
        return self.replace_metadata_in_section(metadata, template)

    def datatype_path(self, data_type):

        source_dir = self.config.datatype_sourcedir(data_type)
        file_name = self.config.datatype_filename(data_type)
        if not source_dir:
            source_dir = self.get_deterministic_folder(file_name)

        return os.path.join(
            self.config.datatype_basedir(data_type),
            source_dir,
            file_name,
        )

    def datatype_filename_template(self, project_name):
        # self.logger.debug('this is project filename ', project_name)
        self.logger.debug(self.config.datatype_filename(project_name))
        self.logger.debug(self.config.datatype_reblocks(project_name))
        self.logger.debug(self.config.datatype_regex(project_name))
        template = Template(
            Template(self.config.datatype_filename(project_name)).safe_substitute(
                dict(self.config.datatype_reblocks(project_name).items()),
            ),
        ).safe_substitute(dict(self.config.datatype_regex(project_name).items()))
        self.logger.debug(f"Filename template {template}")
        return template

    def datatype_metadata(self, project_name, file_name):
        """Extract metadata from the file_name for a given project / datatype

        Arguments:
            project_name: str, name of the project /datatype in the config
            file_name: str, name of the file being processed

        Returns:
            metadata dictionary
        """
        self.logger.debug(f"Building metadata file={file_name} project={project_name}")

        if self.config.datatype_extra(project_name) == True:
            query = self.config.datatype_extra_query(project_name)
            query = query % (file_name)
            # self.logger.debug('this is extra query ', query)
            self.logger.debug("- Extra query: {:-<50}".format("%s" % query))
            extra_metadata = list(
                self.db.execute_query(
                    self.config.datatype_extra_query(project_name) % (file_name),
                ),
            )[0]
            template = self.datatype_filename_template(project_name)
            self.logger.debug(template)
            self.logger.info(extra_metadata)
            m = re.match(template, os.path.join(extra_metadata, file_name))

        else:
            template = self.datatype_filename_template(project_name)
            m = re.match(template, file_name)

        if m is None:
            self.logger.info(
                f"file {file_name} does not match project {project_name} specification",
            )
            return None
        else:
            self.logger.debug(f"File {file_name} matched project: {project_name}")
            metadata = m.groupdict()

            if self.config.datatype_extra(project_name) == True:
                extra_metadata_2 = json.loads(
                    list(
                        self.db.execute_query(
                            self.config.datatype_extra_query_2(project_name)
                            % (file_name),
                        ),
                    )[0],
                )
                self.logger.debug(extra_metadata_2)
                metadata.update(extra_metadata_2)

            self.logger.debug(
                f"Metadata for file {file_name} project {project_name}: {metadata}",
            )
            return metadata

    def get_deterministic_folder(self, file_name):
        # stripping out the folder, just in case
        base_file_name = os.path.basename(file_name)
        scope = self.config.rucio_scope

        # https://rucio.github.io/documentation/started/concepts/replica_workflow/#deterministic-algorithm-based-on-hashes
        h = hashlib.md5(f"{scope}:{base_file_name}".encode()).hexdigest()
        return os.path.join(scope, h[:2], h[2:4])
