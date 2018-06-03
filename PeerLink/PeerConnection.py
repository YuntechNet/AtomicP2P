import threading
import time
import socket

class PeerConnection(threading.Thread):
    def __init__(self, HOST,PORT,SendType,Message=''):
        threading.Thread.__init__(self)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        self.finish=False
        self.Message = Message
        self.SendType = SendType

    def run(self):
        while self.finish!=True:
            self.client.send(self.SendType.encode('ascii'))
            DataType = self.client.recv(1024)
            print ("the server say", DataType.decode('ascii'))   
            self.client.send(self.Message)
            Data = self.client.recv(1024)
            print ("the server say", Data.decode('ascii'))   
            EndConnect = self.client.recv(1024)
            print ("the server say", EndConnect.decode('ascii'))         
            if (EndConnect == (b"There are some error, so I can accept it.") or EndConnect == (b"This is a good connection") ):
                self.finish=True
        return