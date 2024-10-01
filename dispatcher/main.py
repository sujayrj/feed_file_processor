# dispatcher/main.py

import yaml
import logging
import sys
from dispatcher.dispatcher_factory import DispatcherFactory
from utils.logger import setup_logging


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <ENVIRONMENT>")
        sys.exit(1)

    environment = sys.argv[1]  # Fetch the environment parameter (DEV, ST, UAT, PROD)
    setup_logging('config/dispatcher_logging.yaml')

    # Load dispatcher config
    try:
        with open('config/dispatcher_config.yaml', 'r') as file:
            config = yaml.safe_load(file)
    except FileNotFoundError as e:
        raise RuntimeError("Dispatcher Configuration file not found : {}".format(str(e)))
    except yaml.YAMLError as e:
        raise RuntimeError("Error parsing YAML file : {}".format(str(e)))
    except Exception as e:
        raise RuntimeError("Unknown error loading Dispatcher configuration : {}".format(str(e)))

    directories = config['directories']

    for directory_config in directories:
        dispatcher = DispatcherFactory.get_dispatcher(directory_config, environment)
        if dispatcher:
            try:
                dispatcher.dispatch()
            except Exception as e:
                logging.getLogger('dispatcher_logger').error(f"Error in processing: {e}")


if __name__ == "__main__":
    main()
