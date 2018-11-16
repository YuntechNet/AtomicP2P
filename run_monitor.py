import socket
from threading import Thread
from prompt_toolkit import prompt
from prompt_toolkit.patch_stdout import patch_stdout

from LibreCisco.utils.manager import ThreadManager


class LoggerRecver(ThreadManager):

    def __init__(self):
        super(LoggerRecver, self).__init__(loopDelay=0.1, auto_register=False,
                                           logger=None)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('localhost', 17032))
        self.sock.listen(1)

    def registerHandler(self):
        pass

    def registerCommand(self):
        pass

    def run(self):
        while not self.stopped.wait(self.loopDelay):
            (conn, addr) = self.sock.accept()
            thread = Thread(target=self.recv, args=(conn, addr))
            thread.start()

    def recv(self, conn, addr):
        while True:
            if self.stopped.is_set() is False:
                msg = conn.recv(1024).decode()
                if msg is not None and msg != '':
                    print(msg)


if __name__ == '__main__':
    logRecver = LoggerRecver()
    logRecver.start()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            with patch_stdout():
                user_input = prompt('> ')
                if user_input.upper() == 'C:CONNECT':
                    sock.connect(('localhost', 17031))
                elif user_input.upper() in ['C:CLOSE', 'C:STOP']:
                    sock.close()
                    logRecver.stop()
                    break
                else:
                    sock.send(user_input.encode())
        except KeyboardInterrupt:
            sock.close()
            logRecver.stop()
            break
