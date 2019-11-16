from ...abc import AuthenticatorABC


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
    """

    def _authenticate_packet(self, sock: "Socket", pkt: "Packet") -> None:
        if pkt.program_hash != self.program_hash and pkt.is_reject() is False:
            return self._on_fail(sock=sock, pkt=pkt)
        else:
            return self._on_pass(sock=sock, pkt=pkt)

    def _on_pass(self, sock: "Socket", pkt: "Packet") -> None:
        return self.on_packet_to_route(sock=sock, pkt=pkt)

    def _on_fail(self, sock: "Socket", pkt: "Packet") -> None:
        self.logger.info(
            "Illegal peer {} with unmatch hash {{{}...{}}} try to "
            "connect to net.".format(
                pkt.src, pkt.program_hash[:6], pkt.program_hash[-6:]
            )
        )
        pkt.redirect_to_host(src=self.server_info.host, dst=pkt.src)
        pkt.set_reject(reject_data="Unmatching peer hash.")
        self.pend_packet(sock=sock, pkt=pkt)
