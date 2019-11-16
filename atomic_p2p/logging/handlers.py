import socket
import errno
from Crypto.Cipher import AES
from logging import Handler, StreamHandler as SHandler


class StreamHandler(SHandler):
    def __init__(self, name, stream=None):
        super().__init__(stream)
        self.name = name


class SocketHandler(Handler):
    def __init__(self, name, password):
        super().__init__()
        self.name = name
        self.password = password
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def new_cipher(self, key: str):
        return AES.new(key.encode(), AES.MODE_CBC, "0000000000000000".encode())

    def encrypt(self, raw_data: str):
        if len(raw_data) % 16 != 0:
            raw_data += " " * (16 - len(raw_data) % 16)
        return self.new_cipher(key=self.password).encrypt(raw_data.encode())

    def emit(self, record):
        log_entry = self.format(record)
        data = self.encrypt(log_entry)
        try:
            self.sock.sendto(data, ("localhost", 17032))
        except Exception:
            pass
