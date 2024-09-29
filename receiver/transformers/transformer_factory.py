from receiver.transformers.base_transformer import BaseTransformer
from receiver.transformers.no_op_transformer import NoOpTransformer
from receiver.transformers.rename_transformer import RenameTransformer

class TransformerFactory:
    @staticmethod
    def get_transformer(type, config):
        if type == 'Rename':
            return RenameTransformer(config)
        elif type == 'None':
            return NoOpTransformer()  # No transformation needed
        else:
            raise ValueError(f"Unknown transformer type: {type}")
