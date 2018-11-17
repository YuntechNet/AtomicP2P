import os
import socket
from threading import Thread

from LibreCisco.utils.manager import ThreadManager
from LibreCisco.utils.logging import getLogger


class LocalMonitor(ThreadManager):

    def __init__(self, service):
        super(LocalMonitor, self).__init__(loopDelay=0.5, auto_register=False,
                                           logger=getLogger(__name__))
        self.service = service
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('localhost', 17031))

    def registerHandler(self):
        pass

    def registerCommand(self):
        pass

    def run(self):
        while not self.stopped.wait(self.loopDelay):
            try:
                (data, addr) = self.sock.recvfrom(1024)
                thread = Thread(target=self.command_recv, args=(data, addr))
                thread.start()
            except OSError as ose:
                if ose.errno == os.errno.EINVAL:
                    break

    def stop(self):
        super(LocalMonitor, self).stop()
        self.sock.close()

    def command_recv(self, data, addr):
        if data is not None and data != '':
            result = self.service.onProcess(data.decode())[1]
            res_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            res_sock.sendto(str(result).encode(), ('localhost', 17032))
            res_sock.close()
