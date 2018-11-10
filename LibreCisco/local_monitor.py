import socket
from threading import Thread
from LibreCisco.utils.manager import ThreadManager
from LibreCisco.utils.logging import getLogger


class LocalMonitor(ThreadManager):

    def __init__(self, service):
        super(LocalMonitor, self).__init__(loopDelay=10, auto_register=False,
                                           logger=getLogger(__name__))
        self.service = service
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('localhost', 17031))
        self.sock.listen(1)

    def registerHandler(self):
        pass

    def registerCommand(self):
        pass

    def run(self):
        while not self.stopped.wait(self.loopDelay):
            (conn, addr) = self.sock.accept()
            thread = Thread(target=self.command_recv, args=(conn, addr))
            thread.start()

    def command_recv(self, conn, addr):
        while True:
            try:
                msg = conn.recv(1024).decode()
                if msg is not None and msg != '':
                    result = self.service.onProcess(msg)
                    self.logger.info(result)
            except Exception as e:
                break
        conn.close()
