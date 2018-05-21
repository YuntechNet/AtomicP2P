import threading
import time
import socket

class Client(threading.Thread):
    def __init__(self, HOST,PORT,Message):
        threading.Thread.__init__(self)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        self.finish=False
        self.cmd = Message

    def run(self):
        while self.finish!=True:
            self.client.send(self.cmd.encode('ascii'))
            data = self.client.recv(1024)
            print (data.decode('ascii'))
            if data.decode('ascii')=="server received you message.":
                self.finish=True
        return