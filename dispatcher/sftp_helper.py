import paramiko
from utils.logger import get_logger

class SFTPHelper:
    def __init__(self, server_config):
        self.hostname = server_config['hostname']
        self.username = server_config['username']
        self.ssh_key_path = server_config['ssh_key_path']
        self.port = server_config.get('port', 22)
        self.sftp = None
        self.logger = get_logger('dispatcher_logger')

    def __enter__(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                hostname=self.hostname,
                username=self.username,
                key_filename=self.ssh_key_path,
                port=self.port
            )
            self.sftp = self.client.open_sftp()
            return self
        except paramiko.AuthenticationException as e:
            self.logger.error(f"Authentication failed while connecting to {self.hostname}: {str(e)}")
            raise
        except paramiko.SSHException as e:
            self.logger.error(f"Error establishing SSH connection to {self.hostname}: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unknown error connecting to {self.hostname}: {str(e)}")
            raise

    def upload_file(self, local_file, remote_path):
        try:
            self.sftp.put(local_file.as_posix(), remote_path)
        except FileNotFoundError as e:
            self.logger.error(f"File not found: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Error uploading file {local_file} to {remote_path}: {str(e)}")
            raise

    def __exit__(self, exc_type, exc_value, traceback):
        if self.sftp:
            self.sftp.close()
        if self.client:
            self.client.close()
