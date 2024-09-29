from .base_dispatcher import BaseDispatcher
from sftp_helper import SFTPHelper

class SFTPDispatcher(BaseDispatcher):
    def transfer(self, destination_details, server_config):
        """Transfer files to an external server via SFTP."""
        try:
            destination_path = destination_details['destination_path']
            files_to_transfer = self.find_files_to_transfer()

            with SFTPHelper(server_config) as sftp:
                for file in files_to_transfer:
                    try:
                        sftp.upload_file(file, destination_path)
                        self.logger.info(f"Transferred {file.name} to external server at {destination_path}")
                    except Exception as e:
                        self.logger.error(f"Failed to transfer {file.name} to {destination_path}: {str(e)}")
                        continue  # Skip to next file

            # Delete corresponding trigger files after successful transfer
            self.delete_trigger_files(files_to_transfer)

        except Exception as e:
            self.logger.error(f"Error in SFTPDispatcher: {str(e)}")
            raise
