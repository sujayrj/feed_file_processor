from .shared_drive_dispatcher import SharedDriveDispatcher
from .sftp_dispatcher import SFTPDispatcher
from utils.server_config_loader import ServerConfigLoader
import logging


class DispatcherFactory:
    @staticmethod
    def get_dispatcher(directory_config, environment):
        """
        Factory method to load dispatcher based on destination type and environment.

        :param directory_config: Directory configuration from YAML.
        :param environment: The environment string (DEV, ST, UAT, PROD).
        :return: An instance of the appropriate dispatcher class.
        """
        if not directory_config['enabled']:
            logging.getLogger('dispatcher_logger').info(
                f"Transfer disabled for: {directory_config['source_directory']}")
            return None
        try:
            if directory_config['destination_type'] == 'shared_drive':
                return SharedDriveDispatcher(directory_config, environment)
            elif directory_config['destination_type'] == 'external_server':
                server_config = ServerConfigLoader.get_server_info()  # Load external server details
                return SFTPDispatcher(directory_config, environment), server_config
            else:
                raise ValueError("Unknown destination type: {}".format(directory_config['destination_type']))

        except KeyError as e:
            raise ValueError(f"Missing configuration key: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Error in DispatcherFactory: {str(e)}")
