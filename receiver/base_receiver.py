import os
from abc import ABC, abstractmethod
from pathlib import Path

class BaseReceiver(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def process_files(self):
        """Process the files according to specific receiver logic."""
        pass

    def validate_directory(self, directory_path):
        """Validate that the directory exists."""
        directory = Path(directory_path)
        if not directory.exists():
            self.logger.error(f"Directory {directory} does not exist.")
            return False
        return True
