import socket
import errno
from Crypto.Cipher import AES
from logging import Handler, StreamHandler as SHandler


class StreamHandler(SHandler):

    def __init__(self, name, stream=None):
        super(StreamHandler, self).__init__(stream)
        self.name = name


class SocketHandler(Handler):

    def __init__(self, name, password):
        super(SocketHandler, self).__init__()
        self.name = name
        self.cipher = AES.new(password, AES.MODE_CBC,
                              '0000000000000000'.encode())
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def encrypt(self, raw_data):
        if len(raw_data) % 16 != 0:
            raw_data += ' ' * (16 - len(raw_data) % 16)
        return self.cipher.encrypt(raw_data)

    def emit(self, record):
        log_entry = self.format(record)
        data = self.encrypt(log_entry)
        try:
            self.sock.sendto(data, ('localhost', 17032))
        except Exception as e:
            pass
