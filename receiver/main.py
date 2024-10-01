import yaml
from receiver.receiver_factory import ReceiverFactory
from utils.logger import setup_logging

def main():
    setup_logging('../config/receiver_logging.yaml')

    # Load configuration from YAML
    try:
        with open('../config/receiver_config.yaml', 'r') as config_file:
            config = yaml.safe_load(config_file)
    except FileNotFoundError as e:
        raise RuntimeError("Receiver Configuration file not found : {}".format(str(e)))
    except yaml.YAMLError as e:
        raise RuntimeError("Error parsing YAML file : {}".format(str(e)))
    except Exception as e:
        raise RuntimeError("Unknown error loading Receiver configuration : {}".format(str(e)))

    # Iterate over each receiver and process files
    for receiver_config in config['receivers']:
        receiver = ReceiverFactory.get_receiver(receiver_config)
        receiver.process_files()

if __name__ == '__main__':
    main()
