from typing import Tuple
from atomic_p2p.utils import host_valid
from atomic_p2p.utils.communication import Packet


class Handler(object):
    """Base class for every handler
    This class responsible for wrapping / handler pkt send and recieve.
    Including accepted or rejected packet.

    The actual data maintain is by Packet class.
    """

    def __init__(self, peer: 'Peer', pkt_type: str) -> None:
        """Init of Handler class

        Args:
            peer: A Peer object to interact with its inner data.
            pkt_type: A unique string to represent this pkt in peer when proce-
                      ssing packets.
        """
        self.__peer = peer
        self.__pkt_type = pkt_type

    @property
    def peer(self) -> 'Peer':
        return self.__peer

    @property
    def pkt_type(self) -> str:
        return self.__pkt_type

    def on_send(self, target: Tuple[str, int], **kwargs) -> 'Packet':
        if 'reject_data' in locals()['kwargs']:
            return self.on_send_reject_pkt(target=target, **kwargs)
        else:
            return self.on_send_pkt(target=target, **kwargs)

    def on_send_pkt(self, target: Tuple[str, int], **kwargs) -> 'Packet':
        raise NotImplementedError

    def on_send_reject_pkt(self, target: Tuple[str, int],
                           reject_data: object, **kwargs) -> 'Packet':
        packet = Packet(dst=target, src=self.peer.server_info.host, _hash=None,
                        _type=self.pkt_type, _data={})
        packet.set_reject(reject_data=reject_data)
        return packet

    def on_recv(self, src: Tuple[str, int],
                pkt: Packet, sock: 'SSLSocket', **kwargs) -> None:
        """
        Args:
            src: Source host.
            pkt: A Packet object contains all data which recieved.
            sock: A SSLSocket object who recv this pkt.
        """
        assert host_valid(src) is True
        if pkt.is_reject():
            self.on_recv_reject_pkt(src=src, pkt=pkt, conn=sock, **kwargs)
        else:
            self.on_recv_pkt(src=src, pkt=pkt, conn=sock, **kwargs)

    def on_recv_pkt(self, src: Tuple[str, int], pkt: 'Packet',
                    conn: 'SSLSocket', **kwargs) -> None:
        raise NotImplementedError

    def on_recv_reject_pkt(self, src: Tuple[str, int], pkt: 'Packet',
                           conn: 'SSLSocket', **kwargs) -> None:
        reject = pkt.data['reject']
        self.__peer.logger.info('Rejected by {}, reason: {}'.format(
            pkt.src, reject))
        # TODO: Fit unittest empty conn in PeerInfo
        #       Waiting for use mock.
        #                      - 2019/04/13
        if conn is not None:
            self.peer.pend_socket_to_rm(sock=conn)
