import socket
import errno
from logging import Handler, StreamHandler as SHandler


class StreamHandler(SHandler):

    def __init__(self, name, stream=None):
        super(StreamHandler, self).__init__(stream)
        self.name = name


class SocketHandler(Handler):

    def __init__(self, name):
        super(SocketHandler, self).__init__()
        self.name = name
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def emit(self, record):
        log_entry = self.format(record)
        try:
            self.sock.sendto(log_entry.encode(), ('localhost', 17032))
        except Exception as e:
            pass
