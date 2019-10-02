from atomic_p2p.abc import AuthenticatorABC
from atomic_p2p.mixin.topology.lan import (
    JoinHandler,
    CheckJoinHandler,
    NewMemberHandler,
    AckNewMemberHandler,
)


class DefaultAuthenticatorMixin(AuthenticatorABC):
    """DefaultAuthenticatorMixin
    This class provide a peer's ability to decide a packet is allow to be process
     by higer layer in Peer or not.
    
    The class which inherit this mixin should contain some fileds and methods:
        (A) fields:
            (1) program_hash: a hash str for recognize packet is safe or not.
                    Usually a hash of whole program can prevent Man-in-Middle attack.
            (2) logger: logger for everything.
        (B) methods:
            (1) _on_packet: The method to keep process packet to higher level when
                    authenticate success.
            (2) pend_packet: The method to queue a socket to process schedule of a Peer.
            (3) is_peer_in_net: The method to check a peer in net or not.
    """

    def _authenticate_packet(self, sock: "SSLSocket", pkt: "Packet") -> None:
        if pkt.is_reject() is False:
            if pkt.program_hash != self.program_hash:
                return self._on_unmatch_hash(sock=sock, pkt=pkt)
            elif self.is_peer_in_net(info=pkt.src) is False and pkt._type not in [
                JoinHandler.pkt_type,
                CheckJoinHandler.pkt_type,
                NewMemberHandler.pkt_type,
                AckNewMemberHandler.pkt_type,
            ]:
                return self._on_not_in_net(sock=sock, pkt=pkt)
        return self._on_pass(sock=sock, pkt=pkt)

    def _on_pass(self, sock: "SSLSocket", pkt: "Packet") -> None:
        return self.on_packet_to_route(sock=sock, pkt=pkt)

    def _on_fail(self, sock: "SSLSocket", pkt: "Packet") -> None:
        pass

    def _on_unmatch_hash(self, sock: "SSLSocket", pkt: "Packet") -> None:
        self.logger.info(
            "Illegal peer {} with unmatch hash {{{}...{}}} try to "
            "connect to net.".format(
                pkt.src, pkt.program_hash[:6], pkt.program_hash[-6:]
            )
        )
        pkt.redirect_to_host(src=self.server_info.host, dst=pkt.src)
        pkt.set_reject(reject_data="Unmatching peer hash.")
        self.pend_packet(sock=sock, pkt=pkt)

    def _on_not_in_net(self, sock: "SSLSocket", pkt: "Packet") -> None:
        self.logger.info(
            "Illegal peer {} not in net try to connect to net.".format(pkt.src)
        )
        pkt.set_reject(reject_data="Not in current net.")
        self.pend_packet(sock=sock, pkt=pkt)
