#!/usr/bin/env python
from __future__ import annotations

import argparse
import linecache
import logging.config
import os.path
import sys
import unittest
import uuid
from datetime import datetime
from typing import Dict
from typing import Optional
from typing import Union
from urllib.parse import urlparse
from urllib.parse import urlunsplit

import yaml
from tqdm import tqdm

# Import Rucio dependencies
os.environ["RUCIO_HOME"] = os.path.expanduser("~/rucio")
from rucio.rse import rsemanager as rsemgr
from rucio.common.utils import generate_uuid
from rucio.client.ruleclient import RuleClient
from rucio.client.replicaclient import ReplicaClient
from rucio.client.didclient import DIDClient
from rucio.client.client import Client
from rucio.common.exception import DataIdentifierNotFound, DuplicateContent
from gfal2 import Gfal2Context

# import Classes
from transfer_agents.metadata import MetaData
from transfer_agents.es_query import EsData
from transfer_agents.config import get_config_file, RucioClientConfig

REPLICATION_BATCH_SIZE = 10


def remove_slash(some_text):
    """Remove starting / at the beginning of a text"""
    if some_text.startswith("/"):
        return some_text[1:]
    else:
        return some_text


class RucioClientInconsistentReplicas(Exception):
    def __init__(self, org_check, dest_check, file_name):
        super().__init__(
            f"Inconsistent state of replicas of {file_name}: origin={org_check} dest={dest_check}",
        )


class RucioData:
    def __init__(
        self,
        config: RucioClientConfig,
        es_body: str = get_config_file("es_body.json"),
        csv_file: str = None,
    ):

        self.config = config
        self.logger = logging.getLogger("rucio_functions")

        # Gfal context
        self.gfal = Gfal2Context()

        # Rucio Configuration
        self.client = Client()

        self.metadata = MetaData(config=config, csv_file=csv_file)
        self.es = EsData(config=config, es_body=es_body)

    def check_scope(self):
        """
        Check if the scope exists, otherwise create it
        """

        scope = self.config.rucio_scope

        self.logger.debug(f'Checking scope "{scope}"')

        if self.config.rucio_scope not in self.client.list_scopes_for_account(
            account=self.config.rucio_account,
        ):
            self.logger.info(f'scope "{scope}" needs to be created')

            self.client.add_scope(
                self.config.rucio_account,
                self.config.rucio_scope,
            )
        else:
            self.logger.debug(f'Scope "{scope}" already exists')

    def rucio_add_metadata(self, did, metadata_dict):
        self.logger.info(f"Adding metadata to DID {did}")
        for key, value in metadata_dict.items():
            self.logger.debug(
                f"adding metadata key={key} with value={value} to did {did}",
            )

            self.client.set_metadata(
                scope=self.config.rucio_scope,
                name=did,
                key=key,
                value=value,
                recursive=False,
            )

    def rucio_list_rules(self):
        return list(self.client.list_account_rules(account=self.config.rucio_account))

    def rucio_rule_exists(self, did_name, single_rse):
        """Check if a replication rule exists

        Arguments:
            did_name: str, name of the DID affected by the rule
            single_rse: str, RSE expression

        Returns:
            rule id or False
        """
        rule_list = list(
            self.client.list_replication_rules(
                {
                    "scope": self.config.rucio_scope,
                    "name": did_name,
                    "rse_expression": single_rse,
                },
            ),
        )
        if rule_list:
            return rule_list[0]["id"]
        else:
            return False

    def rucio_rse_url(self, rse, path=None):
        """
        Return the base path of the rucio url

        Arguments:
            rse: str, RSE name
            path: str, optional, path inside the RSE

        Returns:
            str, url to RSE resource, e.g. root://localhost:1094/rucio/test.root

        WARNING: picking the first protocol
        """
        rse_settings = rsemgr.get_rse_info(rse)
        protocol = rse_settings["protocols"][0]
        rse_url = "{scheme}://{hostname}:{port}{prefix}".format(**protocol)

        # Adding the path manually
        # otherwise it could strip out the prefix
        if path is not None:
            if path[0] != "/":
                path = "/" + path
            rse_url += path

        return rse_url

    def rucio_check_replica(self, did, single_rse=None, all_states=False):
        """
        Check if a replica of the given file at the site already exists.
        """

        self.logger.debug(f"Checking replica of did={did} in rse={single_rse}")
        if all_states:
            self.logger.debug(f"Accepting all states in replica check")

        replicas = self.client.list_replicas(
            [{"scope": self.config.rucio_scope, "name": did}],
            rse_expression=single_rse,
            all_states=all_states,
        )

        for replica in replicas:
            if isinstance(replica, dict) and single_rse in replica["rses"]:
                path = replica["rses"][single_rse][0]
                state = replica["states"][single_rse]
                self.logger.info(
                    f"Found replica: did={did} rse={single_rse} state={state}",
                )
                return path
        self.logger.info(
            f"Did not find a replica of did={did} in rse={single_rse}",
        )
        return False

    def rucio_tombstone_source_replica(self, name):
        """Mark a DID for deletion at source RSE"""

        # If deletion at source is not enabled skip it
        if not self.config.rucio_delsource:
            return None

        # Generic config
        rse = self.config.rucio_sourcerse
        scope = self.config.rucio_scope

        # Check if replica exists at source to avoid error
        has_replica = self.rucio_check_replica(name, rse, all_states=True)
        if has_replica:
            self.client.set_tombstone(
                [
                    {
                        "name": name,
                        "scope": scope,
                        "rse": rse,
                    },
                ],
            )
            self.logger.info(
                f"Set tombstone on replica of DID: {scope}:{name} at RSE: {rse}",
            )
        else:
            self.logger.debug(
                f"Could not set tombstone on replica of DID: {scope}:{name} at RSE: {rse}",
            )

    def rucio_file_stat(
        self,
        name: str,
        sourcefile: str,
        checksum: str | None = None,
        size: int | None = None,
    ) -> dict[str, str | int]:
        """
        Get the size and checksum for every file in the run from defined path
        """
        """
        generate the registration of the file in a RSE :
        :param rse: the RSE name.
        :param scope: The scope of the file.
        :param name: The name of the file.
        :param bytes: The size in bytes.
        :param adler32: adler32 checksum.
        :param pfn: PFN of the file for non deterministic RSE  
        :param dsn: is the dataset name.
        """
        # Obtener el checksum y tamaño si están presentes, de lo contrario, usar los valores predeterminados
        if checksum is not None:
            adler32_checksum: str = checksum
        else:
            self.logger.debug(f"Getting checksum of {sourcefile}")
            adler32_checksum: str = self.gfal.checksum(sourcefile, "adler32")
            self.logger.debug(
                f"Successfully got checksum of {sourcefile} = {adler32_checksum}",
            )

        if size is not None:
            file_size: int = size
        else:
            self.logger.debug(f"Getting file size of {sourcefile}")
            file_size: int = self.gfal.stat(sourcefile).st_size
            self.logger.debug(
                f"Successfully got file size of {sourcefile} = {file_size}",
            )

        # Crear el diccionario replica con los valores obtenidos
        replica: dict[str, str | int] = {
            "scope": self.config.rucio_scope,
            "name": name,
            "adler32": adler32_checksum,
            "bytes": file_size,
            "meta": {"guid": str(generate_uuid())},
            "pfn": sourcefile,
        }

        return replica

    def rucio_create_dataset(self, name_dataset):
        """Create a dataset, handle if it already exists

        Arguments:
            name_dataset: str, name of the dataset

        Returns:
            dataset
        """

        self.logger.debug(
            "Checking if a provided dataset exists: %s for a scope %s"
            % (name_dataset, self.config.rucio_scope),
        )

        try:
            dataset = self.client.get_did(self.config.rucio_scope, name_dataset)

            if dataset.get("type") == "DATASET":
                self.logger.debug(
                    f"Dataset {name_dataset} already exists in scope {self.config.rucio_scope}",
                )
            else:
                raise Exception(
                    f"DID already exists and it is not a dataset: {dataset}",
                )

        except DataIdentifierNotFound:

            dataset = self.client.add_dataset(
                scope=self.config.rucio_scope,
                name=name_dataset,
            )
            self.logger.info(
                f"Dataset {name_dataset}  succesfully created",
            )

        return dataset

    def rucio_create_container(self, name_container):
        """
        creation of a container :
        :param name_container: the container's name
        """
        self.logger.debug(
            "Checking if a provided container exists: %s for a scope %s"
            % (name_container, self.config.rucio_scope),
        )

        try:
            container = self.client.get_did(self.config.rucio_scope, name_container)

            if container.get("type") == "CONTAINER":
                self.logger.debug(
                    f"Container {name_container} already exists in scope {self.config.rucio_scope}",
                )
            else:
                raise Exception(
                    f"DID already exists and it is not a container: {container}",
                )

        except DataIdentifierNotFound:

            container = self.client.add_container(
                scope=self.config.rucio_scope,
                name=name_container,
            )
            self.logger.info(
                f"Container {name_container}  succesfully created",
            )

        return container

    def rucio_attach_did(self, file_name, dataset_name):
        """
        Attaching a DID to a Collection
        """

        self.logger.info(f"- - - Attaching {file_name} to {dataset_name}")

        try:
            self.client.attach_dids(
                scope=self.config.rucio_scope,
                name=dataset_name,
                dids=[{"scope": self.config.rucio_scope, "name": file_name}],
            )
            self.logger.info(
                f"{file_name} succesfully attached to {dataset_name}",
            )
        except DuplicateContent as e:
            self.logger.info(
                f"{file_name} already attached to {dataset_name}",
            )

    def rucio_collections(self, did, collections):
        """
        Create parent dataset / container structure for a DID

        WARNING: datasets have to come before containers
        We trust that the order in the config file is preserved

        TODO: transform collections into a list
        """
        self.logger.debug(f"Creating collections {collections} for did {did}")
        for collection_id, collection_name in collections.items():
            if "dataset" in collection_id:
                # Create the dataset and containers for the file
                self.rucio_create_dataset(collection_name)

            else:
                self.rucio_create_container(collection_name)

            # Attach the dataset and containers for the file
            self.rucio_attach_did(did, collection_name)
            did = collection_name

    def rucio_add_rule(
        self,
        single_rse,
        did_name,
        purge=True,
        priority=3,
        asynchronous=False,
        source_replica_expression=None,
    ):
        """
        Create a replication rule for a DID at a destination RSE
        """
        did = self.client.get_did(scope=self.config.rucio_scope, name=did_name)
        self.logger.info(
            f"Creating replica rule for {did['type']} {did_name} at rse: {single_rse}",
        )
        rule_id = self.rucio_rule_exists(did_name, single_rse)

        if rule_id:
            self.logger.info(f"Rule for {did_name} already exists at rse: {single_rse}")
            return rule_id

        else:
            rule = self.client.add_replication_rule(
                [{"scope": self.config.rucio_scope, "name": did_name}],
                copies=1,
                rse_expression=single_rse,
                grouping="ALL",
                account=self.config.rucio_account,
                purge_replicas=purge,
                priority=priority,
                asynchronous=asynchronous,
                source_replica_expression=source_replica_expression,
            )
            self.logger.info(
                f"Rule for {did_name} at {single_rse} successfully added with id {rule[0]}",
            )
            return rule[0]

    def origin_replica_needed(self, org_check, dest_check, file_name):
        """Small logic to check if replica at origin is needed"""
        if org_check:
            # Replica at origin already exists no need to create another one
            return False
        elif dest_check and self.config.rucio_delsource:
            # Replica at destination exists and
            # has already been deleted from origin
            return False
        elif dest_check and not self.config.rucio_delsource:
            # File has been removed from origin
            # but origin deletion is not enabled
            raise RucioClientInconsistentReplicas(
                org_check,
                dest_check,
                file_name,
            )
        else:
            # File has not been processed yet
            return True

    def replication_files_rucio(self):
        """Launch the replication from source to destination RSE"""
        dest_rse = self.config.rucio_destrse

        # Build the list of files to transfer
        list_of_files = self.metadata.list_files()
        num_files = len(list_of_files)
        self.logger.info(
            f"Replicating these number of files: {num_files}",
        )

        for file in list_of_files:
            file_name = file["name"]
            self.logger.debug(f"Processing file {file_name}")

            self.logger.debug("Getting source and destination routes")
            dest_name = remove_slash(file["destpfn"])
            sourcepfn = remove_slash(file["sourcepfn"])
            sourcepfn = self.rucio_rse_url(
                self.config.rucio_sourcerse,
                sourcepfn,
            )
            destpfn = self.rucio_rse_url(dest_rse, dest_name)

            self.logger.info(
                f"Replicating file {file_name} from source {sourcepfn} to dest {destpfn}",
            )

            # Check existence of replica at origin
            # accept only available replicas
            org_check = self.rucio_check_replica(
                dest_name,
                single_rse=self.config.rucio_sourcerse,
            )

            # Check existence at destination RSE
            # Accept all states, maybe the replica is
            # not available yet
            dest_check = self.rucio_check_replica(
                did=dest_name,
                single_rse=dest_rse,
                all_states=True,
            )

            # Else, if the file is not registered
            if self.origin_replica_needed(org_check, dest_check, file_name):

                # Get necessary data to create the replica
                # basically checksum and file size
                checksum = file.get("checksum", None)
                size = file.get("size", None)
                file_data = self.rucio_file_stat(
                    dest_name,
                    sourcepfn,
                    size=size,
                    checksum=checksum,
                )
                self.logger.info(
                    f"Registering file with data: {file_data}",
                )

                # Register the replica in the RSE
                add = self.client.add_replicas(
                    rse=self.config.rucio_sourcerse,
                    files=[file_data],
                    ignore_availability=True,
                )

                self.logger.info(file_data)
                self.logger.info(
                    f"Registered succesfully at RSE {self.config.rucio_sourcerse}, file {add}",
                )

                # Add metadata from experiments
                file.setdefault("metadata", {})
                file["metadata"]["replication_time"] = datetime.today().strftime(
                    "%Y%m%dT%H%M%S",
                )
                self.rucio_add_metadata(dest_name, file["metadata"])

                # Adding dataset/container structure
                self.rucio_collections(
                    dest_name,
                    file["organization"],
                )

            # If there's no replica at the destination RSE
            # create a rule that will force its creation
            if dest_check is False:

                self.rucio_add_rule(
                    dest_rse,
                    file["collection"],
                    priority=file["priority"],
                    asynchronous=False,
                )

                # Mark the replica at source RSE for deletion, if configured
                # To be done after the creation of replication rule

                self.rucio_tombstone_source_replica(dest_name)
