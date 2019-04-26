from LibreCisco.utils import printText, host_valid
from LibreCisco.utils.communication import Packet


class Handler(object):
    """Base class for every handler
    This class responsible for wrapping / handler pkt send and recieve.
    Including accepted or rejected packet.

    The actual data maintain is by Packet class.
    """

    def __init__(self, peer, pkt_type):
        """Init of Handler class
        Args:
            peer: A Peer object to interact with its inner data.
            pkt_type: A unique string to represent this pkt in peer when proce-
                      ssing packets.
        """
        self.__peer = peer
        self.__pkt_type = pkt_type

    @property
    def peer(self):
        return self.__peer

    @property
    def pkt_type(self):
        return self.__pkt_type

    def on_send(self, target, **kwargs):
        if 'reject_data' in locals()['kwargs']:
            return self.on_send_reject_pkt(target=target, **kwargs)
        else:
            return self.on_send_pkt(target=target, **kwargs)

    def on_send_pkt(self, target, **kwargs):
        raise NotImplementedError

    def on_send_reject_pkt(self, target, reject_data, **kwargs):
        packet = Packet(dst=target, src=self.peer.server_info.host, _hash=None,
                        _type=self.pkt_type, _data={})
        packet.set_reject(reject_data=reject_data)
        return packet

    def on_recv(self, src, pkt, sock, **kwargs):
        """
        Args:
            src: A tuple of (str, int) represents source host.
            pkt: A Packet object contains all data which recieved.
            sock: A socket object who recv this pkt.
        """
        assert host_valid(src) is True
        if pkt.is_reject():
            self.on_recv_reject_pkt(src=src, pkt=pkt, conn=sock, **kwargs)
        else:
            self.on_recv_pkt(src=src, pkt=pkt, conn=sock, **kwargs)

    def on_recv_pkt(self, src, pkt, conn, **kwargs):
        raise NotImplementedError

    def on_recv_reject_pkt(self, src, pkt, conn, **kwargs):
        reject = pkt.data['reject']
        printText('Rejected by {}, reason: {}'.format(pkt.src, reject))
        # TODO: Fit unittest empty conn in PeerInfo
        #       Waiting for use mock.
        #                      - 2019/04/13
        if conn is not None:
            self.peer.pend_socket_to_rm(sock=conn)
