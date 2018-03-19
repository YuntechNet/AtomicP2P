import socket

from Config import Config
from utils.Enums import LogLevel
from utils.Manager import ProcessManager

class LibServer(ProcessManager):

    def __init__(self, outputQueue, host, port, sleep=0.5):
        ProcessManager.__init__(self, 'LibServer', outputQueue)
        self.sleep = sleep

        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKER, socket.SO_REUSEADDR, 1)
        self.print('Socket created on host: %s' % host)

        try:
            self.sock.bind((self.host, self.port))
        except socket.error as err:
            self.print('Bind failed. Error Code : ' .format(err))

        self.sock.listen(10)
        self.print("Socket Listening on port %d" % self.port)

    def run(self): # Override
        while not self.stopped.wait(self.sleep):
            conn, addr = self.sock.accept()
            try:
                conn.send(bytes("Message"+"\r\n",'UTF-8'))
                self.print("Message sent")
                data = conn.recv(1024)
                self.print(data.decode(encoding='UTF-8'))
            except socket.error as e:
                self.print(e)
            self.sock.close()

    # The best way to stop a block-socket server is connect to itself and close
    # connection to let code keep running to next loop to detect stop signal.
    def exit(self):
        super(LibServer, self).exit()
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.host, self.port))
        self.sock.close()

