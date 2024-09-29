# utils/server_config_loader.py

import yaml
import os


class ServerConfigLoader:
    """Class to load server configurations for external transfers (like SFTP)."""

    @staticmethod
    def get_server_info(config):
        """
        Retrieves server information for an external transfer from the server config file.

        :param config: The config object containing details such as server name.
        :return: Dictionary containing server connection details (host, port, username, etc.)
        """
        server_name = config.get('server_name')
        server_config_path = config.get('server_config_path','config/server_info.yaml')  # Default path to server config file

        if not os.path.exists(server_config_path):
            raise FileNotFoundError(f"Server config file not found: {server_config_path}")

        with open(server_config_path, 'r') as file:
            server_configs = yaml.safe_load(file)

        server_info = server_configs.get(server_name)

        if not server_info:
            raise ValueError(f"No server configuration found for server: {server_name}")

        return server_info
