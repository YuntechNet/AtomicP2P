from argparse import ArgumentParser
from sys import exit, stderr

from . import AtomicP2P
from .peer.entity import PeerRole
from .communication import valid_ipv4_format
from .logging import getLogger
from .local_monitor import LocalMonitor
from .utils import DNSResolver


def min_length(data):
    if len(data) % 16 != 0:
        return data + " " * (16 - len(data) % 16)
    else:
        return data


parser = ArgumentParser(prog="python3 -m atomic_p2p")
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
args, left = parser.parse_known_args()

role = PeerRole.CORE
host = args.host
bind_address =args.bind_address
target = args.target
name = "core"
cert = args.cert
auto_start = args.auto_start
auto_join_net = args.auto_join_net
local_monitor_bind_address = args.local_monitor_bind_address
local_monitor_bind_port = args.local_monitor_bind_port
local_monitor_password = args.local_monitor_password

try:
    logger = getLogger(
        name="AtomicP2P",
        local_monitor_password=local_monitor_password,
        local_monitor_bind_port=local_monitor_bind_port,
    )

    dns_resolver = DNSResolver(ns=["127.0.0.1"])
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

    atomic_p2p = AtomicP2P(
        dns_resolver=dns_resolver,
        role=role,
        bind_address=bind_address,
        host=host,
        name=name,
        cert=cert,
        logger=logger,
    )

    if local_monitor_password is not None:
        local_monitor = LocalMonitor(
            service=atomic_p2p,
            bind_address=local_monitor_bind_address,
            bind_port=local_monitor_bind_port,
            password=local_monitor_password,
            logger=logger,
        )
        atomic_p2p.services["local_monitor"] = local_monitor

    if auto_start is True:
        atomic_p2p.start()
    if auto_join_net is True and target is not None:
        if auto_start is False:
            atomic_p2p.start()
        atomic_p2p._on_command(["peer", "join", target])
except Exception as e:
    print("Critical Error:\n{}".format(e), file=stderr)
    exit(1)
