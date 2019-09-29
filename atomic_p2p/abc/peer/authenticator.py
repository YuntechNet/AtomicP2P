from abc import ABC, abstractmethod


class AuthenticatorABC(ABC):
    """Authenticator Absctract Class
    The absctract class for implementation.
    """

    @abstractmethod
    def _authenticate_packet(self, pkt: "Packet", **kwargs) -> None:
        """The function for authenticate a packet.
        Actual examine logic is in this function, and after if-statement will
        call _on_pass method or _on_fail method to make flow control.
        """
        pass

    @abstractmethod
    def _on_pass(self, sock: "SSLSocket", pkt: "Packet", **kwargs) -> None:
        """The method will be execute when authentication passed."""
        pass

    @abstractmethod
    def _on_fail(self, sock: "SSLSocket", pkt: "Packet", **kwargs) -> None:
        """The method will be execute when authentication failed."""
        pass
