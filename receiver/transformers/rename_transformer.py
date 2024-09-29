import os
import re
from datetime import datetime
from pathlib import Path

from receiver.transformers.base_transformer import BaseTransformer
from utils.file_utils import copy_file
from utils.logger import get_logger


class RenameTransformer(BaseTransformer):
    def __init__(self, config):
        self.rename_pattern = config['process_config']['rename_pattern']
        self.logger = get_logger('receiver_logger')

    def transform(self, src_file, dest_dir):
        sequence_number = self.get_last_sequence_number(dest_dir, self.rename_pattern)
        new_dat_file_name = self.build_filename(self.rename_pattern, sequence_number)
        new_trg_file_name = new_dat_file_name.replace('.csv', '.trg')

        src_trg_file = src_file.with_suffix('.trg')

        dat_dest_file = os.path.join(dest_dir, new_dat_file_name)
        trg_dest_file = os.path.join(dest_dir, new_trg_file_name)

        copy_file(src_file, dat_dest_file)
        copy_file(src_trg_file, trg_dest_file)

        self.logger.info(f"Successfully copied and processed {src_file} and {dat_dest_file} to {dest_dir}")
        self.logger.info(f"Successfully copied and processed {src_trg_file} and {trg_dest_file} to {dest_dir}")

    from datetime import datetime
    from pathlib import Path
    import re

    def get_last_sequence_number(self, dest_path, file_pattern):
        """Find the latest sequence number from the destination files matching initials and current date."""
        try:
            path = Path(dest_path)
            sequences = []

            # Extract the initial part of the filename (before '_<nnnnn>')
            initial_pattern = re.match(r'([A-Za-z0-9]+)_', file_pattern)
            if not initial_pattern:
                self.logger.error(f"Unable to extract initial part from file pattern: {file_pattern}")
                return 1

            initial_part = initial_pattern.group(1)

            # Get current date in YYMMDD format
            current_date = datetime.now().strftime("%y%m%d")

            # Compile regex to match the initial part, current date, and extract <nnnnn> sequence number
            sequence_regex = re.compile(rf'{initial_part}_{current_date}_(\d{{5}})_\d{{2}}\(\d{{4}}\)\.csv')

            for file in path.iterdir():
                if file.is_file() and file.name.endswith('.csv'):
                    self.logger.debug(f"Trying to match pattern: {sequence_regex.pattern} with file: {file.name}")

                    # Attempt to match the filename based on the initial part, date, and .csv
                    match = sequence_regex.match(file.name)
                    if match:
                        seq_number = match.group(1)  # Extract the <nnnnn> part
                        self.logger.debug(f"Found sequence number: {seq_number}")
                        sequences.append(int(seq_number))
                    else:
                        self.logger.debug(f"No match for file: {file.name}")

            # Return the max sequence number incremented by 1 or 00001 if none found
            return max(sequences) + 1 if sequences else 1

        except Exception as e:
            self.logger.error(f"Error getting last sequence number from {dest_path}: {str(e)}")
            return 1

    def build_filename(self, pattern, seq_num):
        """Generate a new filename based on the pattern and sequence number."""
        date = datetime.now().strftime('%y%m%d')
        mmdd = datetime.now().strftime('%m%d')
        return pattern.replace('YYMMDD', date).replace('<nnnnn>', f'{seq_num:05d}').replace('MMDD', mmdd)
