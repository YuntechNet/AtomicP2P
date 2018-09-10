import threading
import time
import socket
import pickle

class PeerConnection(threading.Thread):
    def __init__(self, host,port,sendType,message=''):
        threading.Thread.__init__(self)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.sendMessage = [sendType, message]

    def run(self):
        self.connection( pickle.dumps(self.sendMessage))

    def connection(self, data):
        self.client.send(data)
        Data = self.client.recv(1024)
        data = Data.decode('ascii')
        if data != '':
            print ("the server say", data)   
