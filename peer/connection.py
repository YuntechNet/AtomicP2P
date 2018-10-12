import threading
import time
import socket
import pickle
from peer.message import Message

class PeerConnection(threading.Thread):

    def __init__(self, host='',port='',sendType='',message=''):
        super(PeerConnection, self).__init__()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if type(message) == Message:
            self.message = message
            self.client.connect(self.message._ip)
        else:
            self.client.connect((host, port))
            self.sendMessage = [sendType, message]

    def run(self):
        if hasattr(self, 'message'):
            self.connection(data=self.message)
        else:
            self.connection( pickle.dumps(self.sendMessage))

    def connection(self, data):
        if type(data) == Message:
            self.client.send(str.encode(Message.send(data)))
        else:
            self.client.send(data)
        Data = self.client.recv(1024)
        data = Data.decode('ascii')
        if data != '':
            print ("the server say", data)   

