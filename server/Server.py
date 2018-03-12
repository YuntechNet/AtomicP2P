import socket

from Config import Config
from utils.Manager import ProcessManager

class LibServer(ProcessManager):

    def __init__(self, outputQueue, host, port, sleep=0.5):
        ProcessManager.__init__(self, 'LibServer', outputQueue)
        self.sleep = sleep

        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
            self.conn.close()

