import threading
import time
import socket
import pickle
from peer.message import Message

class PeerConnection(threading.Thread):

    def __init__(self, message=''):
        super(PeerConnection, self).__init__()
        self.message = message
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.message._ip)

    def run(self):
        self.connection(data=self.message)

    def connection(self, data):
        self.client.send(Message.send(data))
        Data = self.client.recv(1024)
        data = Data.decode('ascii')
        if data != '':
            print ("the server say", data)   

