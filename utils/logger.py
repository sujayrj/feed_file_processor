import logging
import logging.config
import yaml
import os


def setup_logging(path, default_level=logging.INFO):
    try:
        if os.path.exists(path):
            with open(path, 'r') as f:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)
    except Exception as e:
        print(f"Error in setting up logging configuration: {str(e)}")
        logging.basicConfig(level=default_level)


def get_logger(name):
    return logging.getLogger(name)
