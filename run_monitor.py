import socket
from threading import Thread
from prompt_toolkit import prompt
from prompt_toolkit.patch_stdout import patch_stdout

from LibreCisco.utils.manager import ThreadManager


class LoggerRecver(ThreadManager):

    def __init__(self):
        super(LoggerRecver, self).__init__(loopDelay=0.1, auto_register=False,
                                           logger=None)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('localhost', 17032))

    def registerHandler(self):
        pass

    def registerCommand(self):
        pass

    def run(self):
        while not self.stopped.wait(self.loopDelay):
            (data, addr) = self.sock.recvfrom(1024)
            thread = Thread(target=self.recv, args=(data, addr))
            thread.start()

    def recv(self, data, addr):
        if self.stopped.is_set() is False:
            msg = data.decode()
            if msg is not None and msg != '':
                print(msg)


if __name__ == '__main__':
    logRecver = LoggerRecver()
    logRecver.start()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        try:
            with patch_stdout():
                user_input = prompt('> ')
                if user_input.upper() == 'C:CLOSE':
                    sock.close()
                elif user_input.upper() == 'C:STOP':
                    logRecver.stop()
                    break
                else:
                    sock.sendto(user_input.encode(), ('localhost', 17031))
        except KeyboardInterrupt:
            sock.close()
            logRecver.stop()
            break
