from __future__ import annotations

import linecache
import logging
import os
import sys

import psycopg2
import yaml

from transfer_agents.config import get_config_file


class dbData:
    """
    The dbData class provides a connection to a PostgreSQL database and
    functions to query and commit data to the database.
    """

    def __init__(self, config):
        """
        Loads the database configuration from a YAML file.

        Args:
            default_config (str, optional): The file path to the YAML configuration file. Defaults to '../config/sample.yaml'.
        """
        self.config = config
        if "psql" not in self.config:
            raise ValueError("'psql' not found in the configuration file")

        # Create a self.logger with the name `client.agents.list_file`
        self.logger = logging.getLogger("list_file")

    def get_connection(self):
        """_summary_

        Returns:
            _type_: _description_
                    return psycopg2.connect(database="mock",
                            host="mock.pic.es",
                            user="mock",
                            password="mock",
                            port="5432")
        """
        try:
            return psycopg2.connect(**self.config.db_config)
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

    def execute_query(self, query):
        """
        Execute a query on the database and return the result.

        Args:
            query (str): The SQL query to be executed.

        Returns:
            result (set): A set of results returned by the query.
        """
        conn = self.get_connection()

        if conn:
            self.logger.info("Connection to the PostgreSQL established successfully.")
            cursor = conn.cursor()
            try:
                # Execute the query
                self.logger.debug(f"Going to run this query: '{query}'")
                cursor.execute(query)
                # Fetch the results
                result = cursor.fetchall()
                self.logger.debug(f"Query returned these result:\n{result}")
                # Return a set of results, if any
                return {item[0] for item in result} if result else set()
            except Exception as e:
                # Log the error, if any occurred
                self.logger.error(f"An error occurred while executing the query: {e}")
            finally:
                # Close the cursor, regardless of whether an error occurred or not
                cursor.close()
        else:
            # Log an error if the connection could not be established
            self.logger.error("Error establishing connection to the PostgreSQL.")

    def commit_changes(self, query):
        """
        Execute a query on the database and commit the changes.

        Args:
            query (str): The SQL query to be executed.
        """
        conn = self.get_connection()

        if conn:
            self.logger.info("Connection to the PostgreSQL established successfully.")
            cursor = conn.cursor()
            try:
                # Execute the query
                cursor.execute(query)
                # Commit the changes
                conn.commit()
            except Exception as e:
                # Log the error, if any occurred
                self.logger.error(f"An error occurred while committing changes: {e}")
            finally:
                # Close the cursor, regardless of whether an error occurred or not
                cursor.close()
        else:
            # Log an error if the connection could not be established
            self.logger.error("Error establishing connection to the PostgreSQL.")
