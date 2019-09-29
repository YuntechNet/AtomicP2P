from typing import Tuple, List
from traceback import format_exc
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE
from errno import ECONNRESET
from socket import error as sock_error
from ssl import wrap_socket, CERT_REQUIRED, SSLWantReadError
from queue import Queue
from time import sleep
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, SO_REUSEPORT

from atomic_p2p.utils import host_valid
from atomic_p2p.logging import getLogger
from atomic_p2p.communication import Packet
from atomic_p2p.mixin.peer import (
    HandleableMixin,
    CommandableMixin,
    DefaultAuthenticatorMixin,
)

from .entity import PeerInfo, StatusType
from .topology import LanTopologyMixin
from .dns_resolver import DNSResolver
from .command import HelpCmd, JoinCmd, SendCmd, ListCmd, LeaveNetCmd
from .communication import MessageHandler
from .monitor import Monitor


class Peer(
    HandleableMixin, CommandableMixin, LanTopologyMixin, DefaultAuthenticatorMixin
):
    """
    Attributes:
        server_info (PeerInfo): Peer's peer info.
        pkt_handlers (Dict[str, Handler]): All handlers which peer have ability
            to process.
        peer_pool (Dict[Tuple[str, int], PeerInfo]): All peers currently avai-
            lable in net.
    """
    @property
    def server_info(self):
        return self.__server_info

    @property
    def program_hash(self):
        return self.__program_hash

    @property
    def send_queue(self):
        # def packet_queue(self):
        return self.__packet_queue

    @property
    def connectlist(self) -> List:  # Remember to remove `List` import.
        return self.peer_pool.values()

    def __init__(
        self,
        host: Tuple[str, int],
        name: str,
        role: str,
        cert: Tuple[str, str],
        program_hash: str,
        ns: str,
        auto_register: bool = False,
        logger: "logging.Logger" = getLogger(__name__),
    ) -> None:
        """Init of PeerManager

        Args:
            host: Binding host.
            name: Peer's name in net.
            role: Peer's role in net.
            cert: Cert file's path.
            program_hash: Program self hash to send in packet.
            ns: Nameserver address for resolve DNS.
            logger: Logger for logging.
        """
        super().__init__()
        self.logger = getLogger(name)
        self.__auto_register = auto_register
        self.__selector = DefaultSelector()
        self.__packet_queue = {}

        self.__cert = cert
        self.__program_hash = program_hash
        self.__server_info = PeerInfo(host=host, name=name, role=role)
        self.__tcp_server = self.__bind_socket(cert=self.__cert)

        self.peer_pool = {}
        self.pkt_handlers = {}
        self.commands = {}

        self.logger.info(
            "Program hash: {{{}...{}}}".format(
                self.__program_hash[:6], self.__program_hash[-6:]
            )
        )
        self.dns_resolver = DNSResolver(ns="127.0.0.1" if ns is None else ns, role=role)
        self.monitor = Monitor(peer=self, logger=getLogger(name + ".MONITOR"))

        if self.__auto_register is False:
            self.logger.warning(
                (
                    "auto_register parameter is set to False,\n You may need to r"
                    "egister them through _register_command & _register_handler m"
                    "ethod."
                )
            )

    def _preregister_handler(self) -> None:
        self.topology_register_handler()
        installing_handlers = [MessageHandler(self)]
        for each in installing_handlers:
            self.register_handler(handler=each)

    def _preregister_command(self) -> None:
        installing_commands = [
            HelpCmd(self),
            JoinCmd(self),
            SendCmd(self),
            ListCmd(self),
            LeaveNetCmd(self),
        ]
        for each in installing_commands:
            self.register_command(command=each)

    def pend_packet(self, sock: "Socket", pkt: "Packet", **kwargs) -> None:
        """Pending pkt's raw_data to queue's with sepecific sock.
        Any exception when wrapping handler to packet whould cause this connec-
        tion been close and thread maintaining loop terminate.

        Args:
            sock: A Socket which wants to pend on its queue.
            pkt: A Packet ready to be pend.
            **kwargs: Any additional arguments needs by handler object.
        
        Raises:
            AssertionError:
                If given pkt variable is not in proper Packet type.
        """
        assert type(pkt) is Packet
        try:
            self.__packet_queue[sock].put_nowait(pkt)
        except Exception:
            self.logger.info(format_exc())

    def register_socket(self, sock: "Socket") -> None:
        """Register a new socket with packet queue & selector.
        Init a packet queue and put into dict for further handling of packets.
        And the given socket will be register in selector for IO process.

        Args:
            sock: A Socket object which wants to be register.
        """
        self.__packet_queue[sock] = Queue()
        self.__selector.register(sock, EVENT_READ | EVENT_WRITE, self.__on_handle)

    def unregister_socket(self, sock: "Socket") -> None:
        del self.__packet_queue[sock]
        self.__selector.unregister(sock)

    def _on_packet(self, sock: "Socket", pkt: "Packet", handler: "Handler") -> None:
        """Method use to process passed packet to higher application layer.
        This method will call by AuthenticatorMixin when a packet is passed examination.
        
        This is 3rd layer to process packet to handler. This is last layer to application layer.
        """
        handler.on_recv(src=pkt.src, pkt=pkt, sock=sock)
        self.monitor.on_recv_pkt(addr=pkt.src, pkt=pkt, conn=sock)

    def new_tcp_long_conn(self, dst: Tuple[str, int]) -> "SSLSocket":
        """Create a ssl-wrapped TCP socket with given destination host

        Args:
            dst: Specified socket destination.

        Returns:
            A SSLSocket object which connected to destination host with
                non-blocking.

        Raises:
            AssertionError:
                If given dst variable is not in proper Tuple[str, int] type.
        """
        assert host_valid(dst) is True
        unwrap_socket = socket(AF_INET, SOCK_STREAM)
        sock = wrap_socket(
            unwrap_socket, cert_reqs=CERT_REQUIRED, ca_certs=self.__cert[0]
        )

        sock.connect(dst)
        sock.setblocking(False)
        return sock

    def loop_start(self):
        self.logger.info(self.__server_info)
        self.__selector.register(self.__tcp_server, EVENT_READ, self.__on_accept)
        if self.__auto_register is True:
            self._preregister_handler()
            self._preregister_command()

        if self.monitor.is_start() is False:
            self.monitor.start()

        self.logger.info("Peer started.")

    def loop(self):
        return self._loop()

    def _loop(self):
        """Called inside infinite loop from outside inherited class.
        It's use to call the method which given event is triggered.
        """
        events = self.__selector.select(timeout=0)
        for key, mask in events:
            if callable(key.data):
                key.data(key.fileobj, mask)

    def loop_stop(self):
        for _, value in self.__packet_queue.items():
            if value.empty() is False:
                sleep(2)
                return self.loop_stop()

        self.__selector.unregister(self.__tcp_server)
        self.leave_net()

        self.monitor.stop()

    def loop_stop_post(self):
        self.__tcp_server.close()
        self.__selector.close()

    def __bind_socket(self, cert: Tuple[str, str]) -> "SSLSocket":
        unwrap_socket = socket(AF_INET, SOCK_STREAM)
        unwrap_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        unwrap_socket.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        unwrap_socket.bind(self.__server_info.host)
        unwrap_socket.listen(5)
        unwrap_socket.setblocking(False)

        self.logger.info("Peer prepared")
        self.logger.info(
            "This peer is running with certificate at path {}".format(cert[0])
        )
        self.logger.info("Please make sure other peers have same certicate.")
        return wrap_socket(
            unwrap_socket, certfile=cert[0], keyfile=cert[1], server_side=True
        )

    def __on_accept(self, sock: "Socket", mask, **kwargs):
        """Call when a new socket is connection by waiter socket.
        This will accept all sockets from outside, but it doesn't mean every socket's
         packet be process by higher layer.
        This is the 1st layer to process sockets.
        """
        conn, _ = sock.accept()
        conn.setblocking(False)
        self.register_socket(sock=conn)

    def __on_handle(self, sock: "Socket", mask, **kwargs):
        """Decide whether send or recv."""
        if mask & EVENT_READ == EVENT_READ:
            self.__on_recv(sock=sock, mask=mask, **kwargs)
        if mask & EVENT_WRITE == EVENT_WRITE:
            self.__on_send(sock=sock, mask=mask, **kwargs)

    def __on_recv(self, sock: "Socket", mask, **kwargs):
        """Method use when recieve socket data.
        This is 2th layer to process Packets.
        """
        try:
            raw_data = sock.recv(4096)
            if raw_data == b"":
                return
            pkt = Packet.deserilize(raw_data=raw_data)
            return self._authenticate_packet(sock=sock, pkt=pkt)
        except SSLWantReadError:
            return
        except sock_error as sock_err:
            if sock_err.errno == ECONNRESET:
                peer_info = self.get_peer_info_by_conn(conn=sock)
                if peer_info is not None:
                    peer_info.status.update(status_type=StatusType.NO_RESP)
                    self.logger.warning(
                        "Peer {} Connection Reseted.".format(peer_info.host)
                    )
            else:
                raise sock_err
        except Exception:
            self.logger.warning(str(self.server_info) + format_exc())

    def __on_send(self, sock: "Socket", mask, **kwargs):
        """Method use when sending data to socket."""
        q = self.__packet_queue[sock] if sock in self.__packet_queue else None
        while q is not None and q.empty() is False:
            try:
                pkt = q.get_nowait()
                handler = self.select_handler(pkt_type=pkt._type)
                handler.pre_send(pkt=pkt)
                data = Packet.serilize(obj=pkt)
                sock.send(data)
                handler.post_send(pkt=pkt, sock=sock)
            except sock_error as sock_err:
                if sock_err.errno == ECONNRESET:
                    q.put_nowait(pkt)
                    self.monitor.peer_status_update_by_host(
                        host=pkt.src, status_type=StatusType.NO_RESP
                    )
                    self.logger.warning("Peer {} Connection Reseted.".format(pkt.src))
                else:
                    raise sock_err
            except Exception:
                self.logger.warning(format_exc())
