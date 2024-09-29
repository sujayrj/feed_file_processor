from .shared_drive_dispatcher import SharedDriveDispatcher
from .sftp_dispatcher import SFTPDispatcher
from utils.server_config_loader import ServerConfigLoader
import logging


class DispatcherFactory:
    @staticmethod
    def get_dispatcher(directory_config):
        if not directory_config['enabled']:
            logging.getLogger('dispatcher_logger').info(
                f"Transfer disabled for: {directory_config['source_directory']}")
            return None
        try:
            source_directory = directory_config['source_directory']
            file_extension = directory_config['file_extension']
            trigger_extension = directory_config['trigger_extension']

            if directory_config['destination_type'] == 'shared_drive':
                return SharedDriveDispatcher(source_directory, file_extension, trigger_extension)
            elif directory_config['destination_type'] == 'external_server':
                server_config = ServerConfigLoader.get_server_info()  # Load external server details
                return SFTPDispatcher(source_directory, file_extension, trigger_extension), server_config
            else:
                raise ValueError("Unknown destination type: {}".format(directory_config['destination_type']))

        except KeyError as e:
            raise ValueError(f"Missing configuration key: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Error in DispatcherFactory: {str(e)}")
