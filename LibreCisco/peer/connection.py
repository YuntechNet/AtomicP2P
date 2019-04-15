import traceback
import threading
import socket
import ssl

from LibreCisco.peer.monitor.peer_status import StatusType
from LibreCisco.utils.communication import Message


class PeerConnection(threading.Thread):

    def __init__(self, peer, message, cert_pem):
        super(PeerConnection, self).__init__()
        self.logger = peer.logger
        self.peer = peer
        self.message = message
        unwrap_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = ssl.wrap_socket(unwrap_socket,
                                      cert_reqs=ssl.CERT_REQUIRED,
                                      ca_certs=cert_pem)
        self.addr = (self.message._to[0], int(self.message._to[1]))

    def run(self):
        def except_process(data):
            status, peer_info = self.peer.monitor.getStatusByHost(data._to)
            if status:
                status.update(status_type=StatusType.PENDING)

        try:
            data = self.message
            self.client.connect(self.addr)
            self.client.send(Message.send(data))
        except ConnectionRefusedError:
            except_process(data)
        except ConnectionResetError:
            except_process(data)
        except Exception as e:
            self.logger.warning(traceback.format_exc())
            except_process(data)
        finally:
            self.client.close()
