import yaml
from dispatcher.dispatcher_factory import DispatcherFactory
from utils.logger import setup_logging

def main():
    # Set up logging
    setup_logging(path='config/dispatcher_logging.yaml')

    # Load dispatcher configuration
    try:
        with open('../config/dispatcher_config.yaml', 'r') as f:
            dispatcher_config = yaml.safe_load(f)
    except FileNotFoundError as e:
        raise RuntimeError(f"Dispatcher configuration file not found: {str(e)}")
    except yaml.YAMLError as e:
        raise RuntimeError(f"Error parsing YAML file: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unknown error loading dispatcher configuration: {str(e)}")

    for directory_config in dispatcher_config['directories']:
        if directory_config.get('enabled', False):
            try:
                dispatcher= DispatcherFactory.get_dispatcher(directory_config)
                dispatcher.transfer(directory_config['destination_details'])
            except Exception as e:
                # Log error and continue with the next directory
                dispatcher.logger.error(f"Error processing directory {directory_config['source_directory']}: {str(e)}")
                continue

if __name__ == "__main__":
    main()
