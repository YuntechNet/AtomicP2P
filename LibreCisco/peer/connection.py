import threading
import socket
import ssl

from LibreCisco.utils import printText
from LibreCisco.utils.message import Message

class PeerConnection(threading.Thread):

    def __init__(self, message, cert_pem, output_field):
        super(PeerConnection, self).__init__()
        self.message = message
        self.output_field = output_field
        unwrap_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = ssl.wrap_socket(unwrap_socket, cert_reqs=ssl.CERT_REQUIRED, ca_certs=cert_pem)
        self.client.connect(self.message._to)

    def run(self):
        self.connection(data=self.message)

    def connection(self, data):
        self.client.send(Message.send(data))
        self.client.close()
#        Data = self.client.recv(1024)
#        data = Data.decode('ascii')
#        if data != '':
#            printText("the server say", data)   

