from typing import Tuple, Union, List
from errno import ECONNREFUSED
from socket import error as socket_error

from atomic_p2p.abc import TopologyABC
from atomic_p2p.utils import host_valid
from atomic_p2p.peer.entity import PeerInfo

from .handler import (
    JoinHandler,
    CheckJoinHandler,
    NewMemberHandler,
    AckNewMemberHandler,
    DisconnectHandler,
)

__all__ = ["LanTopologyMixin"]


class LanTopologyMixin(TopologyABC):
    def topology_register_handler(self):
        installing_handlers = [
            JoinHandler(self),
            CheckJoinHandler(self),
            NewMemberHandler(self),
            AckNewMemberHandler(self),
            DisconnectHandler(self),
        ]
        for each in installing_handlers:
            self.register_handler(handler=each)

    def on_packet_to_route(self, sock: "SSLSocket", pkt: "SSLSocket", **kwargs) -> None:
        handler = self.select_handler(pkt_type=pkt._type)
        if handler is None:
            self.logger.info("Unknown packet type: {}".format(pkt._type))
        else:
            return self._on_packet(sock=sock, pkt=pkt, handler=handler)

    def get_peer_info_by_host(
        self, host: Tuple[str, int], **kwargs
    ) -> Union[None, Tuple["SSLSocket", "PeerInfo"]]:
        """Get PeerInfo object from current net's peer_pool if exists.

        Args:
            host: A tuple(str, int) object represents host in net.

        Returns:
            A PeerInfo object get from peer_pool if exists or None.

        Raises:
            ValueError: If a given host is not tuple(str, int) object.
        """
        if self.is_peer_in_net(info=host) is True:
            return self.peer_pool[host]
        else:
            return (None, None)

    def get_peer_info_by_conn(
        self, conn: "SSLSocket", **kwargs
    ) -> Union[None, Tuple["SSLSocket", "PeerInfo"]]:
        for (_, (sock, peer_info)) in self.peer_pool.items():
            if sock == conn:
                return (sock, peer_info)
        return (None, None)

    def is_peer_in_net(
        self, info: Union["PeerInfo", Tuple[str, int]], **kwargs
    ) -> bool:
        """Return if in current net pool

        Args:
            peer_info: A PeerInfo object or a tuple with (str, int) type represents
                host.

        Returns:
            true if in net, or False.

        Raises:
            ValueError: If peer_info's type is not PeerInfo or tuple (str, int)
        """
        if type(info) is tuple:
            return info in self.peer_pool
        elif type(info) is PeerInfo:
            return info.host in self.peer_pool
        else:
            raise ValueError(
                "Parameter peer_info should be tuple with "
                "(str, int) or type PeerInfo"
            )

    def add_peer_in_net(
        self, sock: "SSLSocket", peer_info: "PeerInfo", **kwargs
    ) -> None:
        """Add given PeerInfo into current net's peer_pool.

        Args:
            sock: A SSLSocket object to be add.
            peer_info: A PeerInfo object to be add.

        Raises:
            AssertionError:
                If given peer_info variable is not in proper PeerInfo type.
        """
        assert type(peer_info) is PeerInfo
        self.peer_pool[peer_info.host] = (sock, peer_info)

    def del_peer_in_net(self, peer_info: "PeerInfo", **kwargs) -> bool:
        """Delete given PeerInfo if exists in current net's peer_pool

        Args:
            peer_info: A PeerInfo object to be delete.

        Return:
            True is success, or False.

        Raises:
            ValueError: If peer_info object type is not PeerInfo.
        """
        if self.is_peer_in_net(info=peer_info) is True:
            del self.peer_pool[peer_info.host]
            return True
        else:
            return False

    def handler_unicast_packet(
        self, host: Tuple[str, int], pkt_type: str, **kwargs
    ) -> None:
        """Exported function for pending unicast pkt with specific host.
        This function is for anyother instance to make a safer packet send with
        specific host currently in peer_pool.

        Args:
            host: Destination to recieve packet. This host should be currently
                in  .
            pkt_type: Packet's unique identity str.
            kwargs: Any addtional arguments need by Handler.

        Raises:
            AssertionError:
                If given host variable is not in proper Tuple[str, int] type.
        """
        assert host_valid(host) is True
        handler = self.select_handler(pkt_type=pkt_type)
        if handler is None:
            self.logger.info("Unknow handler pkt_type")
        elif self.is_peer_in_net(info=host) is True:
            sock, _ = self.get_peer_info_by_host(host=host)
            pkt = handler.on_send(target=host, **kwargs)
            self.pend_packet(sock=sock, pkt=pkt)
        else:
            self.logger.info("Host not in current net.")

    def handler_broadcast_packet(
        self, host: Tuple[str, int], pkt_type: str, **kwargs
    ) -> None:
        """Exported function for pending broadcast pkt to specific peers.
        This function is for anyother instance to make a safer packet send with
        given role currently in peer_pool to broadcast.

        Args:from atomic_p2p.utils.logging import getLogger

            host: First argument in tuple will not be used. Only use second one
                which represents target role to recive the pkt.
            pkt_type: Packet's unique identity str.
            kwargs: Any addtional arguments need by Handler.
        """
        handler = self.select_handler(pkt_type=pkt_type)
        if handler is None:
            self.logger.info("Unknow handler pkt_type")
        else:
            for (_, (sock, peer_info)) in self.peer_pool.items():
                if host[1] == "all" or host[1] == peer_info.role:
                    pkt = handler.on_send(target=peer_info.host, **kwargs)
                    self.pend_packet(sock=sock, pkt=pkt)

    def join_net(self, host: Tuple[str, int], **kwargs) -> None:
        """Join into a net with known host.
        This method is use to join a net with known host while current peer is
         not in any net yet.

        Args:
            host: A tuple with address in str at position 0 and port in int at
                  positon 1.
        """
        assert host_valid(host) is True
        handler = self.select_handler(pkt_type=JoinHandler.pkt_type)
        pkt = handler.on_send(target=host)

        sock = self.new_tcp_long_conn(dst=host)
        self.register_socket(sock=sock)
        self.pend_packet(sock=sock, pkt=pkt)

    def join_net_by_DNS(self, domain: str, ns: List[str] = None, **kwargs) -> None:
        """Join into a net with known domain.
        This method is use to join a net with known domain while current peer 
          is not in any net yet.
        The domain can point to single or multiple exists host in net.

        Args:
            domain: The domain point to any host currently in net.
            ns: A list with str, specified which DNS server to query.

        Raises:
            ValueError:
                No any valid record after given domain.
        """
        if ns is not None and type(ns) is list:
            self.dns_resolver.change_ns(ns=ns)
        records = self.dns_resolver.sync_from_DNS(
            current_host=self.server_info.host, domain=domain
        )
        for each in records:
            try:
                return self.join_net(host=each.host)
            except socket_error as sock_err:
                if sock_err.errno == ECONNREFUSED:
                    self.logger.warning("Socket {} is not open.".format(each))
                else:
                    raise sock_err
            except Exception as e:
                raise e
        raise ValueError("No Online peer in DNS records.")

    def leave_net(self, **kwargs) -> None:
        for (_, (sock, _)) in self.peer_pool.items():
            self.unregister_socket(sock=sock)
        self.peer_pool = {}
