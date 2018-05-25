import threading
import time
import socket

class Client(threading.Thread):
    def __init__(self, HOST,PORT,SendType,Message):
        threading.Thread.__init__(self)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        self.finish=False
        self.message = Message
        self.sendtype = SendType

    def run(self):
        while self.finish!=True:
            self.client.send(self.sendtype.encode('ascii'))
            dataT = self.client.recv(1024)
            print (dataT.decode('ascii'))   
            self.client.send(self.message.encode('ascii'))
            data = self.client.recv(1024)
            print (data.decode('ascii'))            
            if (dataT == (b"server know what's type you may send.") and data == (b"server received you message.") ):
                self.finish=True
        return