from .base_dispatcher import BaseDispatcher
from pathlib import Path
import shutil
import logging


class SharedDriveDispatcher(BaseDispatcher):
    def __init__(self, config, environment):
        self.config = config
        self.environment = environment
        self.logger = logging.getLogger('dispatcher_logger')

    def dispatch(self, destination_details):
        """Transfer files to a shared drive."""
        source_directory = self.config['source_directory']
        destination_details = self.config['destination_details']
        file_extension = self.config['file_extension']
        trigger_extension = self.config['trigger_extension']

        try:
            destination_path = Path(destination_details['shared_drive_path'])
            destination_path.mkdir(parents=True, exist_ok=True)

            files_to_transfer = self.find_files_to_transfer()
            for file in files_to_transfer:
                dest_file = destination_path / file.name
                try:
                    shutil.copy2(file, dest_file)
                    self.logger.info(f"Transferred {file.name} to shared drive at {destination_path}")
                except Exception as e:
                    self.logger.error(f"Failed to transfer {file.name} to {destination_path}: {str(e)}")
                    continue  # Skip to next file

            # Delete corresponding trigger files after successful transfer
            self.delete_trigger_files(files_to_transfer)

        except Exception as e:
            self.logger.error(f"Error in SharedDriveDispatcher: {str(e)}")
            raise
