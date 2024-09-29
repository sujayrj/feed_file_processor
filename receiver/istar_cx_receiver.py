import os
import re
import shutil
from pathlib import Path

from receiver.base_receiver import BaseReceiver
from utils.logger import get_logger
from receiver.transformers.transformer_factory import TransformerFactory


class IStarCXReceiver(BaseReceiver):
    def __init__(self, config):
        super().__init__(config)
        self.config = config
        self.logger = get_logger('receiver_logger')
        self.transformer_factory = TransformerFactory()

    def process_files(self):
        # Iterate over all servers defined in the config
        for server in self.config.get('servers', []):
            source_path = server['source_path']
            self.logger.info(f"Processing files from server: {server['server_name']} at path: {source_path}")

            for file_config in server.get('files', []):
                file_name_pattern = file_config['file_name_pattern']

                # Convert the file pattern with placeholders into a regex pattern
                regex_pattern = self.convert_pattern_to_regex(file_name_pattern)

                # Get all files in the source directory that match the pattern
                matched_files = self.get_matching_files(source_path, regex_pattern)

                if not matched_files:
                    self.logger.warning(f"No matching files found for pattern: {file_name_pattern}")
                    continue

                for dat_file in matched_files:
                    trg_file = self.get_trg_file(dat_file)

                    # Check if the .trg file exists
                    if not os.path.exists(os.path.join(source_path, trg_file)):
                        self.logger.warning(f"Skipping {dat_file}: corresponding .trg file {trg_file} not found.")
                        continue

                    self.logger.info(f"Processing file: {dat_file} with .trg file: {trg_file}")
                    # Process the file by copying it to the destination(s)
                    self.copy_and_process_file(source_path, dat_file, file_config)

                    # After processing, remove the .trg file
                    trg_file_path = os.path.join(source_path, trg_file)
                    self.remove_trg_file(trg_file_path)

    def convert_pattern_to_regex(self, file_name_pattern):
        """
        Converts a file name pattern with 'nn' and 'hhmm' to a regex pattern.
        """
        # Replace 'nn' with regex for two digits and 'hhmm' with regex for four digits
        regex_pattern = file_name_pattern.replace('nn', r'\d{2}').replace('hhmm', r'\d{4}')
        return re.compile(regex_pattern)

    def get_matching_files(self, source_path, regex_pattern):
        """
        Returns a list of files in the source_path that match the regex pattern.
        """
        try:
            files = os.listdir(source_path)
            return [f for f in files if regex_pattern.match(f) and f.endswith('.dat')]
        except Exception as e:
            self.logger.error(f"Error listing files in {source_path}: {str(e)}")
            return []

    def get_trg_file(self, dat_file):
        """
        Given a .dat file, returns the corresponding .trg file name.
        """
        return dat_file.replace('.dat', '.trg')

    def copy_and_process_file(self, source_path, dat_file, file_config):
        """
        Copies the .dat file and the corresponding .trg file to each destination and processes the .dat file.
        """
        source_file_path = Path(source_path) / dat_file
        trg_file_path = source_file_path.with_suffix('.trg')  # Get the corresponding .trg file

        # Validate the source directory using the BaseReceiver's method
        if not self.validate_directory(source_path):
            self.logger.error(f"Source directory {source_path} does not exist. Skipping file: {dat_file}")
            return

        if not trg_file_path.exists():
            self.logger.warning(f"Corresponding .trg file not found for {dat_file}. Skipping.")
            return

        for destination in file_config.get('destination', []):
            destination_path = Path(destination['path'])  # Convert destination to Path object
            should_process = destination['should_process']

            try:
                # Get the last sequence number from the destination directory
                # last_sequence_number = get_last_sequence_number(destination_path, dat_file)
                # new_sequence_number = last_sequence_number + 1  # Increment for the new file

                # Create the transformer instance based on the process type
                transformer = self.transformer_factory.get_transformer(should_process, destination)

                # Add the new sequence number to the destination config before transformation
                # destination['process_config']['new_sequence_number'] = new_sequence_number

                # Try-catch block for processing and copying
                try:
                    # Apply transformation (e.g., renaming) for the .dat file
                    transformer.transform(source_file_path, destination.get('path'))

                except Exception as process_error:
                    # Log and skip this file, continue with the next one
                    self.logger.error(f"Error processing file {dat_file} or {trg_file_path.name}: {process_error}")
                    continue  # Continue to the next destination

            except Exception as dest_error:
                # Handle errors related to specific destination logic (e.g., sequence number retrieval)
                self.logger.error(f"Failed to process {dat_file} for destination {destination_path}: {dest_error}")
                continue  # Continue with the next file

    def remove_trg_file(self, trg_file_path):
        """
        Removes the .trg file after the corresponding .dat file has been processed.
        """
        try:
            os.remove(trg_file_path)
            self.logger.info(f"Removed .trg file: {trg_file_path}")
        except Exception as e:
            self.logger.error(f"Failed to remove .trg file: {trg_file_path}: {str(e)}")
