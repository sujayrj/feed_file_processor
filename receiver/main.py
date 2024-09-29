import yaml
from receiver.receiver_factory import ReceiverFactory
from utils.logger import setup_logging

def main():
    setup_logging('../config/receiver_logging.yaml')

    # Load configuration from YAML
    with open('../config/receiver_config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    # Iterate over each receiver and process files
    for receiver_config in config['receivers']:
        receiver = ReceiverFactory.get_receiver(receiver_config)
        receiver.process_files()

if __name__ == '__main__':
    main()
