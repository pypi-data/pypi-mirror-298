from __future__ import annotations

import logging.config
import os

import yaml


class NonImplementedExtensionError(Exception):
    def __init__(self, ext):
        super().__init__(f"Extension {ext} not implemented")


def get_config_file(f_name: str):
    """Get path to file in config folder"""
    cur_dir = os.path.dirname(__file__)
    return os.path.join(cur_dir, "config_files", f_name)


class Config:
    """
    Base class implementing a configuration object

    The configuration is loaded from a file
    and is accessed like a dictionary
    """

    def __init__(self, config_file):
        self._data = self.load_config(config_file)

    @classmethod
    def load_config(cls, config_file):
        """Read a configuration file into a dictionary-like object"""

        _, ext = os.path.splitext(config_file)
        if ext in [".yml", ".yaml"]:
            with open(config_file) as f:
                return yaml.safe_load(f)
        else:
            raise NonImplementedExtensionError(ext)

    def __getitem__(self, key):
        # Allows dict-like access using brackets, e.g., config['key']
        return self._data[key]

    def __setitem__(self, key, value):
        # Allows setting values like in a dict, e.g., config['key'] = value
        self._data[key] = value

    def __delitem__(self, key):
        # Allows deletion of keys, e.g., del config['key']
        del self._data[key]

    def __contains__(self, key):
        # Allows checking if a key is in the config, e.g., 'key' in config
        return key in self._data

    def __iter__(self):
        # Makes the Configuration object iterable like a dict
        return iter(self._data)

    def __len__(self):
        # Returns the number of items in the configuration
        return len(self._data)

    def get(self, key, default=None):
        # Provides a safe way to get a value with a default
        return self._data.get(key, default)

    def keys(self):
        # Returns the keys in the configuration
        return self._data.keys()

    def values(self):
        # Returns the values in the configuration
        return self._data.values()

    def items(self):
        # Returns the key-value pairs in the configuration
        return self._data.items()

    def __repr__(self):
        return self._data.__repr__()


class RucioClientConfig(Config):
    """
    This class implements specific methods
    and structure for the Rucio client configuration
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.check_config()
        self.setupLogging()

    def setupLogging(self):
        """
        This method sets up the logging configuration for the application.
        """
        if "logging" in self:
            logging.config.dictConfig(self["logging"])

    def check_config(self):
        if "Rucio" not in self:
            raise ValueError("'Rucio' not found in the configuration file")

    # Rucio Section
    @property
    def rucio_section(self):
        return self["Rucio"]

    @property
    def rucio_account(self):
        return self.rucio_section["account"]

    @property
    def rucio_scope(self):
        return self.rucio_section["scope"]

    @property
    def rucio_destrse(self):
        return self.rucio_section["destrse"]

    @property
    def rucio_sourcerse(self):
        return self.rucio_section["sourcerse"]

    @property
    def rucio_delsource(self):
        return self.rucio_section.get("delsource", False)

    # "Data Sections" Section
    @property
    def data_section(self):
        return self["Data Sections"]

    @property
    def datatype_list(self):
        return [
            section
            for section in self.data_section.keys()
            if self.data_section[section]["options"]["basedir"]
            and self.data_section[section]["options"]["transfer"]
        ]

    def datatype_rule(self, data_type):
        return self["Data Sections"][data_type]["options"]["rule_name"]

    def datatype_basedir(self, data_type):
        return self["Data Sections"][data_type]["options"]["basedir"]

    def datatype_transfer(self, data_type):
        return self["Data Sections"][data_type]["options"]["transfer"]

    def datatype_filename(self, data_type):
        return self["Data Sections"][data_type]["options"]["filename"]

    def datatype_sourcedir(self, data_type):
        return self["Data Sections"][data_type]["options"].get("sourcedir")

    def datatype_destdir(self, data_type):
        return self["Data Sections"][data_type]["options"].get("destdir")

    def datatype_priority(self, data_type):
        return self["Data Sections"][data_type]["options"]["priority"]

    def datatype_query(self, data_type):
        return self["Data Sections"][data_type]["options"]["query"]

    def datatype_extra(self, data_type):
        return self["Data Sections"][data_type]["options"]["extra_metadata"]

    def datatype_output_path(self, data_type):
        return self["Data Sections"][data_type]["options"].get("output_path")

    def datatype_metadata(self, data_type):
        return self["Data Sections"][data_type].get("metadata", {})

    def datatype_organization(self, data_type):
        return self["Data Sections"][data_type].get("organization", {})

    def datatype_extra_query(self, data_type):
        return self["Data Sections"][data_type]["extra_metadata"]["query_1"]

    def datatype_extra_query_2(self, data_type):
        return self["Data Sections"][data_type]["extra_metadata"]["query_2"]

    def datatype_regex(self, data_type):
        return self["Data Sections"][data_type].get("regex", {})

    def datatype_reblocks(self, data_type):
        return self["Data Sections"][data_type].get("reblocks", {})

    # psql section
    @property
    def psql_section(self):
        """
        Returns the 'psql' section of the YAML configuration file.

        Returns:
            dict: The 'psql' section of the YAML configuration file.
        """
        return self["psql"]

    @property
    def db_user(self):
        """
        Returns the database username from the YAML configuration file.

        Returns:
            str: The database username.
        """
        return self.psql_section["user"]

    @property
    def db_passwd(self):
        """
        Returns the database password from the YAML configuration file.

        Returns:
            str: The database password.
        """
        return self.psql_section["passwd"]

    @property
    def db_port(self):
        """
        Returns the database port from the YAML configuration file.

        Returns:
            str: The database port.
        """
        return self.psql_section["port"]

    @property
    def db_database(self):
        """
        Returns the database name from the YAML configuration file.

        Returns:
            str: The database name.
        """
        return self.psql_section["db"]

    @property
    def db_host(self):
        """
        Returns the database host from the YAML configuration file.
        """
        return self.psql_section["host"]

    @property
    def db_config(self):
        """
        Initialize the database connection.

        Args:
            host (str): The host name or IP address of the database server.
            database (str): The name of the database.
            user (str): The name of the user.
            password (str): The password for the user.
            port (int, optional): The port number. Defaults to 5432.
        """
        config = {
            "user": self.db_user,
            "host": self.db_host,
            "password": self.db_passwd,
            "database": self.db_database,
        }

        return config

    # elasticsearch section
    @property
    def es_section(self):
        """
        Property to get the Elasticsearch section of the config file.

        Returns:
        Dictionary containing the Elasticsearch config.
        """
        return self["elasticsearch"]

    # Property to return if update states transfer with for Elasticsearch
    @property
    def es_enabled(self):
        """
        Property to get if Elasticsearch is enabled or not.

        Returns:
        Boolean containing for Elasticsearch.
        """
        # return self.templatesection["enabled"]
        return self.es_section.get("enabled", False)

    # Property to return the username for Elasticsearch
    @property
    def es_user(self):
        """
        Property to get the username for Elasticsearch.

        Returns:
        String containing the username for Elasticsearch.
        """
        return self.es_section["user"]

    # Property to return the password for Elasticsearch
    @property
    def es_passwd(self):
        """
        Property to get the password for Elasticsearch.

        Returns:
        String containing the password for Elasticsearch.
        """
        return self.es_section["passwd"]

    # Property to return the schema for Elasticsearch
    @property
    def es_schema(self):
        """
        Property to get the schema for Elasticsearch.

        Returns:
        String containing the schema for Elasticsearch.
        """
        return self.es_section["schema"]

    # Property to return the host for Elasticsearch
    @property
    def es_host(self):
        """
        Property to get the host for Elasticsearch.

        Returns:
        String containing the host for Elasticsearch.
        """
        return self.es_section["host"]

    # Property to return the port for Elasticsearch
    @property
    def es_port(self):
        """
        Property to get the port for Elasticsearch.

        Returns:
        String containing the port for Elasticsearch.
        """
        return self.es_section["port"]

    # Property to return the status of the psql
    @property
    def psql_status(self):
        """
        Property to get the status for psql in Elasticsearch.

        Returns:
        list of transfer status for psql in Elasticsearch.
        """
        return self.es_section["status_changes"]

    def run_es(self):
        return self.es_section["query_search"]

    def es_query_search(self):
        return self.es_section["query_search"]

    def es_query_insert(self):
        return self.es_section["query_insert"]

    def es_query_update(self):
        return self.es_section["query_update"]

    def es_additional_search(self):
        return self.es_section["additional_search"]

    def es_additional_query(self):
        return self.es_section["additional_query"]
