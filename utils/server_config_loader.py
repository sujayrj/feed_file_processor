# utils/server_config_loader.py

import yaml
import os

class ServerConfigLoader:
    """Class to load server configurations for different environments."""

    @staticmethod
    def get_server_info(config, environment):
        """
        Retrieves server information for an external transfer from the server config file.

        :param config: The config object containing details such as server name.
        :param environment: The environment string (DEV, ST, UAT, PROD).
        :return: Dictionary containing server connection details (host, port, username, etc.)
        """
        server_name = config.get('server_name')
        server_config_path = f"config/server_info_{environment}.yaml"  # Construct path based on environment

        if not os.path.exists(server_config_path):
            raise FileNotFoundError(f"Server config file for {environment} not found: {server_config_path}")

        with open(server_config_path, 'r') as file:
            server_configs = yaml.safe_load(file)

        server_info = server_configs.get('servers', {}).get(server_name)

        if not server_info:
            raise ValueError(f"No server configuration found for server: {server_name} in {environment} environment")

        return server_info
