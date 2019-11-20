from .....communication import Handler, Packet
from .....peer.entity import PeerInfo, PeerRole


class AckNewMemberHandler(Handler):
    pkt_type = "peer-ack-new-memeber"

    def __init__(self, peer):
        super().__init__(pkt_type=type(self).pkt_type, peer=peer)

    def on_send_pkt(self, target):
        data = {
            "name": self.peer.server_info.name,
            "role": self.peer.server_info.role.value,
            "listen_port": int(self.peer.server_info.host[1]),
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
        role = PeerRole(data["role"])
        listen_port = int(data["listen_port"])

        peer_info = PeerInfo(
            name=name, role=role, host=(src[0], listen_port), conn=conn
        )
        self.peer.add_peer_in_net(peer_info=peer_info)
        self.peer.logger.info("ACK new member join net: {}".format(peer_info))
