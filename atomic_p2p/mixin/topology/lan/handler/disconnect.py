from typing import Tuple

from atomic_p2p.communication import Packet, Handler


class DisconnectHandler(Handler):
    pkt_type = "peer-disconnect"

    def __init__(self, peer):
        super().__init__(pkt_type=type(self).pkt_type, peer=peer)

    def on_send_pkt(self, target):
        return Packet(
            dst=target,
            src=self.peer.server_info.host,
            program_hash=self.peer.program_hash,
            _type=type(self).pkt_type,
            _data={},
        )

    def __disconnect_unregister(self, host: Tuple[str, int]) -> bool:
        sock, peer_info = self.peer.get_peer_info_by_host(host=host)
        if peer_info is not None:
            self.peer.unregister_socket(sock=sock)
            self.peer.del_peer_in_net(peer_info=peer_info)
            return True
        return False

    def post_send(self, pkt: "Packet", sock: "Socket"):
        if self.__disconnect_unregister(host=pkt.dst) is True:
            self.peer.logger.info("Sended Stop Signal to {}, Stopped.".format(pkt.dst))
        else:
            self.peer.logger.warning("Disconnect failed.")

    def on_recv_pkt(self, src, pkt, conn):
        if self.__disconnect_unregister(host=pkt.src) is True:
            self.peer.logger.info(
                "Received Stop Signal from {}, Stopped.".format(pkt.src)
            )
        else:
            self.peer.logger.warning("Disconnect failed.")
