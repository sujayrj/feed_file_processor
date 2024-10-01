import os
from abc import ABC, abstractmethod
from pathlib import Path
from utils.logger import get_logger


class BaseDispatcher(ABC):
    def __init__(self, config):
        self.source_directory = Path(source_directory)
        self.file_extension = file_extension
        self.trigger_extension = trigger_extension
        self.logger = get_logger('dispatcher_logger')

    @abstractmethod
    def dispatch(self, destination_details):
        """Method to transfer files to the destination."""
        pass

    def find_files_to_transfer(self):
        """Find data files that have corresponding trigger files."""
        try:
            files_to_transfer = []
            files = os.listdir(self.source_directory)
            # for file in files:
            #     if file.endswith(self.file_extension):
            #         trg_file = file.with_suffix(self.trigger_extension)
            #         if trg_file.exists():
            #             files_to_transfer.append(file)
            #         else:
            #             self.logger.warning(f"Trigger file not found for {file.name}")
            # return files_to_transfer

            for file in self.source_directory.glob(f"*{self.file_extension}"):
                trg_file = file.with_suffix(self.trigger_extension)
                if trg_file.exists():
                    files_to_transfer.append(file)
                else:
                    self.logger.warning(f"Trigger file not found for {file.name}")
            return files_to_transfer
        except Exception as e:
            self.logger.error(f"Error while finding files to transfer: {str(e)}")
            raise

    def delete_trigger_files(self, files_to_transfer):
        """Delete the trigger files corresponding to transferred files."""
        for file in files_to_transfer:
            try:
                trigger_file = file.with_suffix(self.trigger_extension)
                if trigger_file.exists():
                    trigger_file.unlink()
                    self.logger.info(f"Deleted trigger file: {trigger_file}")
                else:
                    self.logger.warning(f"Trigger file {trigger_file} not found for deletion.")
            except Exception as e:
                self.logger.error(f"Failed to delete trigger file for {file.name}: {str(e)}")
                continue
