from typing import Tuple, Union, List
from abc import ABC, abstractmethod


class TopologyABC(ABC):
    """Topology Absctract Class
    The absctract class for implementation.

    This abstract class should cowork with HandleableMixin and AuthenticatorABC.
    """

    @abstractmethod
    def topology_register_handler(self):
        """Call by a peer class to register essentials handlers.
        The content should be like:
            installing_handlers = [
                ...
                AnyHandlerYouNeed,
                ...
            ]
            for each in installing_handlers:
                self.register_handler(handler=each)
        Notice that register_handler method is from HandleableMixin &
        each element inside installing_handlers should be a Handler object.
        """

    @abstractmethod
    def on_packet_to_route(self, sock: "Socket", pkt: "Packet", **kwargs):
        """Call by AuthenticatorABC after a packet passed the authentication.
        The content should be like:
            handler = self.select_handler(pkt_type=pkt._type)
            if handler is None:
                self.logger.info("Unknown packet type: {}".format(pkt._type))
            else:
                return handler.on_recv(src=pkt.src, pkt=pkt, sock=sock)
        Notice that select_handler method is from HandleableMixin.
        """

    @abstractmethod
    def get_peer_info_by_host(
        self, host: Tuple[str, int], **kwargs
    ) -> Union[None, "PeerInfo"]:
        """The function get peer info by given host."""

    @abstractmethod
    def get_peer_info_by_conn(
        self, conn: "Socket", **kwargs
    ) -> Union[None, "PeerInfo"]:
        """The function get peer info by given socket."""

    @abstractmethod
    def is_peer_in_net(
        self, info: Union["PeerInfo", Tuple[str, int]], **kwargs
    ) -> bool:
        pass

    @abstractmethod
    def add_peer_in_net(self, peer_info: "PeerInfo", **kwargs) -> None:
        pass

    @abstractmethod
    def del_peer_in_net(self, peer_info: "PeerInfo", **kwargs) -> bool:
        pass

    @abstractmethod
    def handler_unicast_packet(
        self, host: Tuple[str, int], pkt_type: str, **kwargs
    ) -> None:
        pass

    @abstractmethod
    def handler_broadcast_packet(
        self, host: Tuple[str, int], pkt_type: str, **kwargs
    ) -> None:
        pass

    @abstractmethod
    def join_net(self, host: Tuple[str, int], **kwargs) -> None:
        pass

    @abstractmethod
    def join_net_by_DNS(self, domain: str, ns: List[str] = None, **kwargs) -> None:
        pass

    @abstractmethod
    def leave_net(self, **kwargs) -> None:
        pass
