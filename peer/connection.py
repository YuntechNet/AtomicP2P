import threading
import socket
from utils import printText
from utils.message import Message

class PeerConnection(threading.Thread):

    def __init__(self, message, output_field):
        super(PeerConnection, self).__init__()
        self.message = message
        self.output_field = output_field
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.message._host)

    def run(self):
        self.connection(data=self.message)

    def connection(self, data):
        self.client.send(Message.send(data))
        self.client.close()
#        Data = self.client.recv(1024)
#        data = Data.decode('ascii')
#        if data != '':
#            printText("the server say", data)   

