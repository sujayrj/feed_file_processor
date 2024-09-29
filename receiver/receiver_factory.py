from receiver.istar_cx_receiver import IStarCXReceiver

class ReceiverFactory:
    @staticmethod
    def get_receiver(receiver_config):
        receiver_name = receiver_config['name']
        if receiver_name == "i-star cx receiver_system":
            return IStarCXReceiver(receiver_config)
        else:
            raise ValueError(f"Unknown receiver type: {receiver_name}")
