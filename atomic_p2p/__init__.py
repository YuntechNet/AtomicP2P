from typing import Tuple
from os import getcwd
from os.path import join

from .peer import ThreadPeer
from .utils import valid_ipv4_format, create_self_signed_cert as cssc, self_hash


__version__ = "0.0.6"


class AtomicP2P(object):

    # TODO: Arguments need redefine, cause the format is not very clear enough.
    #       Also, whole class should add type hint.
    #                   2019/05/13
    def __init__(
        self,
        dns_resolver: "DNSResolver",
        bind_address: str,
        role: "enum.Enum",
        host: Tuple[str, int],
        name: str,
        cert: str,
        logger: "logging.Logger",
        hash_path: str = join(getcwd(), "atomic_p2p"),
    ) -> None:
        """Init of AtomicP2P object
        Args:
            role: Enum represents peer's role.
            addr: str with `ip:port` format, peer server will listen on.
            name: str represents peer's name.
            cert: str represents cert file's path, should directly point to
                cert file. like `data/atomic_p2p.pem`, and key file should
                same as cert file exception sub-extension with `.key`.
        """
        cert_file, key_file = cssc(
            cert_dir=getcwd(), cert_file=cert, key_file=cert.replace(".pem", ".key")
        )
        self.logger = logger
        self.peer = ThreadPeer(
            dns_resolver=dns_resolver,
            bind_address=bind_address,
            host=host,
            name=name,
            role=role,
            program_hash=self_hash(path=hash_path),
            cert=(cert_file, key_file),
            auto_register=True,
            logger=self.logger,
        )

    def start(self):
        if self.peer.is_start() is False:
            self.peer.start()
        if self.peer.monitor.is_start() is False:
            self.peer.monitor.start()
        if hasattr(self, "local_monitor") is True:
            self.local_monitor = getattr(self, "local_monitor")
            if self.local_monitor.is_start() is False:
                self.local_monitor.start()
        self.logger.info("Platform started.")

    def stop(self):
        if hasattr(self, "local_monitor"):
            self.local_monitor.stop()
        self.peer.monitor.stop()
        self.peer.stop()

    def _on_command(self, cmd):
        if type(cmd) != list and type(cmd) == str:
            cmd = cmd.split(" ")

        service_key = cmd[0].lower()
        if service_key == "peer":
            return (True, self.peer._on_command(cmd[1:]))
        elif service_key == "monitor":
            return (True, self.peer.monitor._on_command(cmd[1:]))
        elif service_key == "stop":
            self.stop()
            return (True, None)
        else:
            help_tips = (
                "peer help            - See peer's help\n"
                "monitor help        - See monitor's help\n"
                "exit/stop            - exit the whole program.\n"
            )
            return (True, help_tips)


def min_length(data):
    if len(data) % 16 != 0:
        return data + " " * (16 - len(data) % 16)
    else:
        return data


def argument_inject(parser: "ArgumentParser"):
    parser.add_argument("host", type=str, help="Service's host.")
    parser.add_argument(
        "-ba",
        "--bind-address",
        default="0.0.0.0",
        type=str,
        help=("The address to bind for peer."),
        dest="bind_address",
    )
    parser.add_argument(
        "-t",
        "--target",
        type=str,
        default="127.0.0.1:8000",
        help="A peer address in net which preparing to join.",
        dest="target",
    )
    parser.add_argument(
        "-c",
        "--cert",
        type=str,
        default="data/atomic_p2p.pem",
        help=(
            "Cert file path."
            "Cert & key should be in same name, but different extension name."
            "And only give pem path is enough."
        ),
        dest="cert",
    )
    parser.add_argument(
        "-as",
        "--auto-start",
        action="store_true",
        default=False,
        help="Auto start whole service.",
    )
    parser.add_argument(
        "-ajn",
        "--auto-join-net",
        action="store_true",
        default=False,
        help="Auto join a with net address",
    )
    parser.add_argument(
        "-lmba",
        "--local-monitor-bind-address",
        type=str,
        default="0.0.0.0",
        help=("The address to bind for local monitor to communicate to."),
        dest="local_monitor_bind_address",
    )
    parser.add_argument(
        "-lmbp",
        "--local-monitor-bind-port",
        type=int,
        default=17031,
        help=("The port to bind for local monitor to communicate to."),
        dest="local_monitor_bind_port",
    )
    parser.add_argument(
        "-lmp",
        "--local-monitor-password",
        type=min_length,
        default=None,
        help=(
            "The password to allow local monitor conntect. "
            "If this password is not set,  local monitor would not be enable."
        ),
        dest="local_monitor_password",
    )
    return parser


def find_host(
    dns_resolver: "DNSResolver", host: str, logger: "logging.Logger"
) -> Tuple[str, int]:
    is_ipv4_host = valid_ipv4_format(host[: host.index(":")] if ":" in host else host)
    if is_ipv4_host is True:
        if ":" not in host:
            raise ValueError(
                (
                    "\tGiven host {{ {} }} is in an IPv4 format but without port given.\n"
                    "\tPlease give a port with :[PORT] surfix like 127.0.0.1:8000"
                ).format(host)
            )
    else:
        if ":" in host:
            logger.warning(
                (
                    "\n\tGiven host {{ {} }} is a domain but give a port.\n"
                    "\tThe given port would be ignore but get from SRV record.\n"
                    "\tPlease sure the DNS record contains SRV record."
                ).format(host)
            )
            host = host[: host.index(":")]
        _, _, port, _ = dns_resolver.srv(fqdn=host)
        if port == -1:
            raise ValueError(
                (
                    "\tGiven domain {{ {} }}'s SRV record is not found,\n"
                    "\tPlease sure domain server is on, and record is valid."
                )
            )
        host = "{}:{}".format(host, port)
    host = host.split(":")
    host[1] = int(host[1])
    return host
