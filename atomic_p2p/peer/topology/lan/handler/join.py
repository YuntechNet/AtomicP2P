from atomic_p2p.communication import Handler, Packet
from atomic_p2p.peer.entity import PeerInfo

from .check_join import CheckJoinHandler
from .new_member import NewMemberHandler


class JoinHandler(Handler):
    pkt_type = "peer-join"

    def __init__(self, peer):
        super().__init__(pkt_type=type(self).pkt_type, peer=peer)
        self.last_join_host = None

    def on_send_pkt(self, target):
        self.peer.logger.info("Joining net to:{}".format(str(target)))
        data = {
            "name": self.peer.server_info.name,
            "listen_port": int(self.peer.server_info.host[1]),
            "role": self.peer.server_info.role,
        }
        return Packet(
            dst=target,
            src=self.peer.server_info.host,
            program_hash=self.peer.program_hash,
            _type=type(self).pkt_type,
            _data=data,
        )

    def post_send(self, pkt: "Packet", sock: "Socket"):
        if pkt.is_reject() is True and "Unmatching peer hash." in pkt.data["reject"]:
            self.peer.unregister_socket(sock=sock)

    def on_recv_pkt(self, src, pkt, conn):
        data = pkt.data
        name = data["name"]
        listen_port = int(data["listen_port"])
        role = data["role"]
        peer_info = PeerInfo(
            name=name, role=role, host=(src[0], listen_port), conn=conn
        )

        self.peer.handler_broadcast_packet(
            host=("", "all"),
            pkt_type=NewMemberHandler.pkt_type,
            **{"peer_info": peer_info},
        )
        self.peer.logger.info(
            "Recieve new peer add request: {}, added.".format(str(peer_info))
        )

        self.peer.add_peer_in_net(peer_info=peer_info)
        self.peer.handler_unicast_packet(
            host=(src[0], listen_port), pkt_type=CheckJoinHandler.pkt_type
        )
