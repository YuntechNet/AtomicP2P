from atomic_p2p.communication import Handler, Packet
from atomic_p2p.peer.entity import PeerInfo

from .ack_new_member import AckNewMemberHandler


class NewMemberHandler(Handler):
    pkt_type = "peer-new-member"

    def __init__(self, peer):
        super().__init__(pkt_type=type(self).pkt_type, peer=peer)

    def _build_accept_packet(self, target, peer_info):
        data = {
            "name": peer_info.name,
            "addr": peer_info.host[0],
            "listen_port": int(peer_info.host[1]),
            "role": peer_info.role,
        }
        return Packet(
            dst=target,
            src=self.peer.server_info.host,
            program_hash=self.peer.program_hash,
            _type=type(self).pkt_type,
            _data=data,
        )

    def on_recv_pkt(self, src, pkt, conn):
        data = pkt.data
        name = data["name"]
        addr = data["addr"]
        listen_port = int(data["listen_port"])
        role = data["role"]

        sock = self.peer.new_tcp_long_conn(dst=(addr, listen_port))
        peer_info = PeerInfo(name=name, role=role, host=(addr, listen_port))

        self.peer.register_socket(sock=sock)
        self.peer.add_peer_in_net(sock=sock, peer_info=peer_info)
        self.peer.handler_unicast_packet(
            host=(addr, listen_port), pkt_type=AckNewMemberHandler.pkt_type
        )
        self.peer.logger.info("New peer join net: {}".format(peer_info))
