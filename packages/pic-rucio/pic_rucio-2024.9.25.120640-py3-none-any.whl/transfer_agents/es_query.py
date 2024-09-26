# Import necessary modules
from __future__ import annotations

import json
import linecache
import logging
import os
import sys
from datetime import datetime
from urllib.parse import urlunsplit

import yaml
from elasticsearch import Elasticsearch

from transfer_agents.config import get_config_file
from transfer_agents.db_functions import dbData

# Import setup logging function
# Import functions from db_functions.py


class EsData:
    """
    Class to manage Elasticsearch queries and connections.
    """

    _config = None

    def __init__(
        self,
        config: RucioClientConfig = None,
        es_body=get_config_file("es_body.json"),
    ):
        """
        Constructor for EsData class.
        Loads the config file and sets the Elasticsearch query body.

        Parameters:
        config (RucioClientConfig): configuration object.
        es_body (str): Path to the Elasticsearch query body JSON file.
        """
        self.config = config
        if "elasticsearch" not in self.config:
            raise ValueError(
                "'elasticsearch' not found in the configuration file",
            )

        # Set up logging for the program
        self.logger = logging.getLogger("es_query")
        # Opening JSON file
        self.es_body = es_body

        # Dictionary to store the status of PostgreSQL queries
        # self.config.psql_status = self.config['elasticsearch']['status_changes']
        # import functions from es_functions.py
        self.db = dbData(config)

    @property
    def mock_run(self):
        return self.config.es_section["mock_run"]

    def es_url(self):
        # Create a list to store the URL components
        elk_url = list()

        # Check if all required values are present
        if None not in (
            self.config.es_schema,
            str(self.config.es_host + ":" + str(self.config.es_port)),
        ):
            # Add the URL components to the list
            elk_url.extend(
                [
                    self.config.es_schema,
                    self.config.es_host + ":" + str(self.config.es_port),
                    "",
                    "",
                    "",
                ],
            )

        # Return the URL as a string
        return urlunsplit(elk_url)

    def connect_elasticsearch(self):
        # Connect to Elasticsearch
        _es = Elasticsearch(
            self.es_url(),
            basic_auth=(self.config.es_user, self.config.es_passwd),
        )

        # Check if the connection was successful
        if _es.ping:
            self.logger.info("Yay Connect to " + self.es_url())
        else:
            self.logger.info("Awww it could not connect!")

        # Return the Elasticsearch connection object
        return _es

    def es_query(self, file_name, file_scope, file_transfer_type):
        # Open the file containing the Elasticsearch query
        body = open(self.es_body)

        # Load the file contents as a dictionary
        es_query = json.load(body)

        # Replace the placeholders in the query with actual values
        es_query = json.loads(json.dumps(es_query).replace("$file_name", file_name))
        es_query = json.loads(json.dumps(es_query).replace("$file_scope", file_scope))
        es_query = json.loads(
            json.dumps(es_query).replace("$file_transfer_type", file_transfer_type),
        )

        # Log the final query
        self.logger.info(es_query)

        # Return the final query
        return es_query

    def process_files(self, scope):
        """
        Processes list of files and performs operations on database.
        """

        print("this is enabled value ", self.config.es_enabled)
        if self.config.es_enabled is True:
            # Loop through each status
            for status in self.config.psql_status:
                self.logger.info(
                    f'Processing status: {self.config.psql_status[status]["pql_id"]}',
                )

                # Get list of files from database
                query = self.config.es_query_search().format(
                    status=self.config.psql_status[status]["pql_id"],
                )
                list_files = self.db.execute_query(query)
                # Loop through each file
                for single_file in list_files:
                    # Query Elasticsearch for file information
                    query = self.es_query(
                        single_file,
                        scope,
                        self.config.psql_status[status]["es_id"],
                    )
                    res = self.connect_elasticsearch().search(
                        index="rucio-*",
                        query=query,
                    )

                    # Get creation date of file from Elasticsearch response
                    created_at = None
                    try:
                        created_at = res["hits"]["hits"][0]["_source"]["created_at"]
                        created_at = datetime.strptime(
                            created_at,
                            "%Y-%m-%dT%H:%M:%S.%f",
                        )
                        created_at = datetime.strftime(created_at, "%Y-%m-%d %H:%M:%S")
                        self.logger.info(created_at)
                    except Exception as e:
                        self.logger.warning(
                            f"No entry found in Elasticsearch for file {single_file}. Error: {e}",
                        )
                    except KeyError as e:
                        self.logger.warning(
                            f"Field not found in Elasticsearch response: {e}",
                        )
                        created_at = None

                    # If additional search is required and creation date is available
                    if self.config.es_additional_search() and created_at:
                        # Perform additional search for file
                        add_query = self.config.es_additional_query()
                        add_query = add_query.format("%s" % single_file)
                        id_files = list(self.db.execute_query(add_query))[0]
                        self.logger.info(id_files)

                        # Prepare insert and update queries
                        in_query = self.config.es_query_insert().format(
                            id_files,
                            created_at,
                            self.config.psql_status[status]["next_status"],
                        )
                        up_query = self.config.es_query_update().format(
                            self.config.psql_status[status]["next_status"],
                            id_files,
                        )
                        self.logger.info(in_query)
                        self.logger.info(up_query)
                        # Execute insert and update queries (if not a mock run)

                    else:
                        # Perform additional search for file
                        up_query = self.config.es_query_update().format(
                            self.config.psql_status[status]["next_status"],
                            created_at,
                            single_file,
                        )

                    if not self.mock_run:
                        self.logger.info(
                            f"Real run, updating and inserting into database (mock run set to {self.mock_run})",
                        )
                        try:
                            self.db.commit_changes(in_query)
                        except Exception:
                            exc_type, exc_obj, tb = sys.exc_info()
                            f = tb.tb_frame
                            lineno = tb.tb_lineno
                            filename = f.f_code.co_filename
                            linecache.checkcache(filename)
                            line = linecache.getline(filename, lineno, f.f_globals)
                            self.logger.warning(
                                f'EXCEPTION IN ({filename}, LINE {lineno} "{line.strip()}"): {exc_obj}',
                            )
                        try:
                            print(up_query)

                            self.db.commit_changes(up_query)
                        except:
                            exc_type, exc_obj, tb = sys.exc_info()
                            f = tb.tb_frame
                            lineno = tb.tb_lineno
                            filename = f.f_code.co_filename
                            linecache.checkcache(filename)
                            line = linecache.getline(filename, lineno, f.f_globals)
                            self.logger.warning(
                                f'EXCEPTION IN ({filename}, LINE {lineno} "{line.strip()}"): {exc_obj}',
                            )
                    else:
                        self.logger.info(
                            "- This is a mock run, no entry will be updated or inserted.",
                        )

        else:
            self.logger.info("Elasticsearch is not enabled, skipping execution.")
