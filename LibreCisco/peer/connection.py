import traceback
import socket
import ssl
from time import sleep

from LibreCisco.peer.entity.peer_status import StatusType
from LibreCisco.peer.communication import (
    JoinHandler, CheckJoinHandler, NewMemberHandler, AckNewMemberHandler,
    DisconnectHandler
)
from LibreCisco.utils import printText, host_valid
from LibreCisco.utils.communication import Packet, Handler
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
        assert host_valid(host) is True

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

                pkt = Packet.deserilize(raw_data=data)
                dst, src, _hash, pkt_type, data = pkt.export
                in_net, hash_match = \
                    self.valid_packet_src(src=src, _hash=_hash)
                handler = self.peer.selectHandler(_type=pkt_type)

                if handler is None:     # Invalid pkt_type
                    printText('Unknown packet type: {}'.format(pkt._type))
                    sleep(3)
                    self.stop()
                    break
                elif hash_match is False and pkt.is_reject() is False:
                    # Invalid hash -> Dangerous peer's pkt.
                    printText('Illegal peer {} with unmatch hash {{{}...{}}}'
                              ' try to connect to net.'.format(
                                    self.host, _hash[:6], _hash[-6:]
                                ))
                    self.sendMessage(host=src, pkt_type=pkt_type, **{
                        'reject_data': 'Unmatching peer hash.'})
                    sleep(3)
                    self.stop()
                    break
                elif in_net is True or type(handler) in [
                        JoinHandler, AckNewMemberHandler, CheckJoinHandler,
                        DisconnectHandler]:
                    # In_net or A join / check_join pkt send.
                    # The exception pkt will be process whether reject or not.
                    handler.on_recv(src=self.host, pkt=pkt, conn=self)
                    self.peer.monitor.on_recv_pkt(addr=pkt.src, pkt=pkt,
                                                  conn=self)
                else:  # Not in net and not exception pkt
                    self.sendMessage(host=src, pkt_type=pkt_type, **{
                        'reject_data': 'Not in current net'})
                    sleep(3)
                    self.stop()
                    break

            except Exception as e:
                print(traceback.format_exc())
        self.conn.close()

    def valid_packet_src(self, src, _hash):
        in_net = self.peer.containsInNet(host=src)
        hash_match = self.peer._hash == _hash
        return in_net, hash_match

    def sendMessage(self, host, pkt_type, **kwargs):
        handler = self.peer.selectHandler(pkt_type)
        if handler:
            pkt = handler.on_send(target=host, **kwargs)
            self.send_packet(pkt=pkt)
        else:
            printText('No such type.')

    def send_packet(self, pkt):
        """Sending pkt by conn.
        Any exception when wrapping handler to packet whould cause this connec-
        tion been close and thread maintaining loop terminate.

        Args:
            pkt: A Packet object ready to be send.
            kwargs: Any additional arguments needs by handler object.
        """
        try:
            assert type(pkt) is Packet
            data = Packet.serilize(obj=pkt)
            self.conn.send(data)
        except Exception as e:
            print(e)
            self.stop()
            self.conn.close()
