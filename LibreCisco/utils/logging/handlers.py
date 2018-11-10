import socket
import errno
from logging import Handler


class SocketHandler(Handler):

    def __init__(self):
        super(SocketHandler, self).__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def emit(self, record):
        log_entry = self.format(record)
        try:
            self.sock.send(log_entry.encode())
        except socket.error as error:
            if error.errno == errno.EPIPE:
                try:
                    self.sock.connect(('localhost', 17032))
                    self.sock.send(log_entry.encode())
                except Exception as e:
                    pass
            else:
                print(error)
