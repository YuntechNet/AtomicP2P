from argparse import ArgumentParser
from sys import exit, stderr

from . import AtomicP2P, argument_inject, find_host
from .peer.entity import PeerRole
from .logging import getLogger
from .local_monitor import LocalMonitor
from .utils import DNSResolver


parser = argument_inject(parser=ArgumentParser(prog="python3 -m atomic_p2p"))
args, left = parser.parse_known_args()

role = PeerRole.CORE
host = args.host
bind_address = args.bind_address
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
    host = find_host(dns_resolver=dns_resolver, host=host, logger=logger)
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
        atomic_p2p.local_monitor = local_monitor

    if auto_start is True:
        atomic_p2p.start()
    if auto_join_net is True and target is not None:
        if auto_start is False:
            atomic_p2p.start()
        atomic_p2p._on_command(["peer", "join", target])
except Exception as e:
    print("Critical Error:\n{}".format(e), file=stderr)
    exit(1)
