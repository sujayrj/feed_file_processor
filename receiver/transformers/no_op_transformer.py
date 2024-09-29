import shutil
import os
from receiver.transformers.base_transformer import BaseTransformer


class NoOpTransformer(BaseTransformer):
    def transform(self, src_file, dest_dir):
        """
        Simply copies the source file to the destination directory without renaming it.
        """
        try:
            # Ensure destination directory exists
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            # Get the original file name
            file_name = os.path.basename(src_file)
            dest_file_path = os.path.join(dest_dir, file_name)

            # Perform the file copy
            shutil.copy2(src_file, dest_file_path)

            # Logging after successful copy
            print(f"Copied file {file_name} to {dest_dir}")

        except Exception as e:
            # Log or handle the error if something goes wrong during copying
            print(f"Failed to copy file {src_file} to {dest_dir}: {e}")
            raise
