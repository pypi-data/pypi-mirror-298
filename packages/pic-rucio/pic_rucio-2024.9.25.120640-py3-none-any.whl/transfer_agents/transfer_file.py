from __future__ import annotations

import csv
import logging
import os

import pandas as pd
import yaml

from transfer_agents.config import get_config_file
from transfer_agents.config import RucioClientConfig


class TransferFile:
    def __init__(
        self,
        config: RucioClientConfig,
        csv_file: str = None,
    ):
        """
        Initializes TransferFile instance.

        Args:
            config (RucioClientConfig, mandatory): configuration object.
            csv_file (str, optional): The file path to the CSV file to validate.
        """

        self.logger = logging.getLogger("TransferFile")
        self.config = config  # Load the YAML configuration file
        self.csv_file = csv_file

    def validate_csv(self):
        """
        Validates the structure of a CSV file.

        Returns:
            list: A list representing the row of the CSV file if the structure is valid, None otherwise.
        """
        if self.csv_file is None:
            self.logger.error("No CSV file provided.")
            return None

        try:
            # Open the CSV file in read mode
            with open(self.csv_file) as file:
                # Create a CSV reader object
                reader = csv.reader(file, delimiter=" ")
                line_number = 0
                for row in reader:
                    line_number += 1
                    # Check if the number of columns is not equal to 3
                    if len(row) != 3:
                        raise ValueError(
                            f"Line {line_number} does not have the correct structure.",
                        )
            # Return None if all lines have correct structure
            return None
        except FileNotFoundError:
            self.logger.error("The specified file was not found.")
            return None
        except Exception as e:
            self.logger.error(f"An error occurred while reading the file: {e}")
            return None

    def get_csv_data(self):
        """
        Reads the CSV file and returns its content as a DataFrame.

        Returns:
            DataFrame: A DataFrame containing the data from the CSV file.
        """
        try:
            df = pd.read_csv(self.csv_file, delimiter=" ", header=None)
            return df
        except FileNotFoundError:
            self.logger.error("The specified file was not found.")
            return None
        except Exception as e:
            self.logger.error(f"An error occurred while reading the file: {e}")
            return None


# Example usage
if __name__ == "__main__":
    default_config = "../config/logging.yaml"  # Specify the logger configuration file
    csv_file = input("Enter the path to the CSV file: ")  # Prompt for the CSV file path
    transfer_file = TransferFile(
        default_config=default_config,
        csv_file=csv_file,
    )  # Create an instance of TransferFile
    csv_structure = (
        transfer_file.validate_csv()
    )  # Validate the structure of the CSV file
    if csv_structure:
        print("CSV file structure validated successfully:")
        print(csv_structure)
