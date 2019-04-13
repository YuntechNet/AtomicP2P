import traceback
import socket
import ssl

from LibreCisco.peer.entity.peer_status import StatusType
from LibreCisco.peer.communication import (
    JoinHandler, CheckJoinHandler, NewMemberHandler, AckNewMemberHandler,
    DisconnectHandler
)
from LibreCisco.utils import printText
from LibreCisco.utils.communication import Message
from LibreCisco.utils.manager import ThreadManager


class PeerTCPLongConn(ThreadManager):
    """PeerTCPLongConn handles detail of a TCP long connection
    This class responsible for every send and recv of each connection.
    Arrtibutes:
        output_field: A output_filed get from peer instance for output infos.
        peer: peer instance get from initializer.
        host: A tuple of this tcp socket connecting to.
        conn: actual socket which get from initializer or later init by host.
    """

    def __init__(self, peer, host, conn, cert_pem=None):
        """Init of PeerTCPLongConn
        Args:
            peer: peer instance get from initializer.
            host: A tuple of this tcp socket connecting to.
            conn: Actual socket which get from initializer,
                  If None, then will be init by host and wrap with cert files.
            cert_perm: If conn is None, then this arg should not be None, in 
                       order to new a socket with ssl wrap.
        """
        super(PeerTCPLongConn, self).__init__(loopDelay=1)
        assert type(host) == tuple
        assert type(host[0]) == str
        assert type(host[1]) == int

        self.output_field = peer.output_field
        self.peer = peer
        self.host = host

        if conn is None:
            assert cert_pem is not None
            unwrap_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn = ssl.wrap_socket(unwrap_socket, cert_reqs=ssl.CERT_REQUIRED,
                                   ca_certs=cert_pem)
            conn.connect(self.host)
        self.conn = conn

    def run(self):
        while not self.stopped.wait(self.loopDelay):
            try:
                data = self.conn.recv(4096)
                if data == b'':
                    continue

                pkt = Message.recv(data)
                in_net = self.peer.containsInConnectlist(self.host[0])
                hash_match = self.peer._hash == pkt._hash
                handler = self.peer.selectHandler(pkt._type)

                if handler:
                    if hash_match is False and pkt.is_reject() is False:
                        printText(
                            ('Illegal peer {} with unmatch hash {{{}...{}}}'
                             'trying to connect to net.').format(
                                self.host, pkt._hash[:6], pkt._hash[-6:]))
                        self.sendMessage(pkt._from, pkt._type, **{
                            'reject_reason': 'Unmatching peer hash.'})
                        self.stop()
                        break
                    elif in_net is True or pkt._type in \
                            [JoinHandler.pkt_type, CheckJoinHandler.pkt_type,
                             AckNewMemberHandler, DisconnectHandler.pkt_type]:
                        handler.onRecv(src=self.host, pkt=pkt,
                                       **{'conn': self})
                        self.peer.monitor.onRecvPkt(addr=pkt._from, pkt=pkt)
                    else:
                        self.sendMessage(
                            host=pkt._from, pkt_type=pkt._type,
                            **{'reject_reason': 'not in current net'})
                else:
                    printText('Unknown packet tpye: {}'.format(pkt._type))
            except Exception as e:
                print(traceback.format_exc())
        self.conn.close()

    def sendMessage(self, host, pkt_type, **kwargs):
        handler = self.peer.selectHandler(pkt_type)
        if handler:
            messages = handler.onSend(target=host, **kwargs)
            for each in messages:
                try:
                    self.conn.send(Message.send(each))
                except Exception:
                    if self.peer.containsInConnectlist(self.host[0]):
                        status, peer_info = \
                            self.peer.monitor.getStatusByHost(self.host[0])
                        if status:
                            status.update(status_type=StatusType.PENDING)
        else:
            printText('No such type.')
