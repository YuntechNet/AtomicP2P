import traceback
import threading
import socket
import ssl

from LibreCisco.peer.monitor.peer_status import StatusType
from LibreCisco.utils import printText
from LibreCisco.utils.communication import Message


class PeerConnection(threading.Thread):

    def __init__(self, peer, message, cert_pem, output_field):
        super(PeerConnection, self).__init__()
        self.peer = peer
        self.message = message
        self.output_field = output_field
        unwrap_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = ssl.wrap_socket(unwrap_socket,
                                      cert_reqs=ssl.CERT_REQUIRED,
                                      ca_certs=cert_pem)
        self.addr = (self.message._to[0], int(self.message._to[1]))

    def run(self):
        try:
            data = self.message
            self.client.connect(self.addr)
            self.client.send(Message.send(data))
        except Exception as e:
            # print(traceback.format_exc())

            status, peer_info = self.peer.monitor.getStatusByHost(data._to)
            if status:
                status.update(status_type=StatusType.PENDING)
        finally:
            self.client.close()
#        Data = self.client.recv(1024)
#        data = Data.decode('ascii')
#        if data != '':
#            printText("the server say", data)
