import socket
import errno
from Crypto.Cipher import AES
from logging import Handler, StreamHandler as SHandler


class StreamHandler(SHandler):
    def __init__(self, name, stream=None):
        super().__init__(stream)
        self.name = name


class SocketHandler(Handler):
    def __init__(
        self, name: str, local_monitor_password: str, local_monitor_bind_port: int
    ):
        super().__init__()
        self.name = name
        self.local_monitor_password = local_monitor_password
        self.local_monitor_bind_port = local_monitor_bind_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def new_cipher(self, key: str):
        return AES.new(key.encode(), AES.MODE_CBC, "0000000000000000".encode())

    def encrypt(self, raw_data: str):
        if len(raw_data) % 16 != 0:
            raw_data += " " * (16 - len(raw_data) % 16)
        return self.new_cipher(key=self.local_monitor_password).encrypt(
            raw_data.encode()
        )

    def emit(self, record):
        log_entry = self.format(record)
        try:
            data = self.encrypt(log_entry)
            self.sock.sendto(data, dst=("localhost", self.local_monitor_bind_port + 1))
        except Exception:
            pass
