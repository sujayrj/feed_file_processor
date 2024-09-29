from abc import ABC, abstractmethod

class BaseTransformer(ABC):
    @abstractmethod
    def transform(self, src_file, dest_dir):
        pass
