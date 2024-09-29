import os
import yaml
import logging.config

def setup_logging(path='../config/receiver_logging.yaml', default_level=logging.INFO):
    """
    Setup logging configuration.
    :param path: Path to the logging configuration file.
    :param default_level: Default logging level if the config file is not found.
    """
    if os.path.exists(path):
        with open(path, 'r') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

# Use this function to get a logger instance
def get_logger(name='receiver_logger'):
    """
    Return a logger instance.
    :param name: Logger name.
    """
    return logging.getLogger(name)
