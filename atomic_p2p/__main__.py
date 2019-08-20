from argparse import ArgumentParser

from atomic_p2p import AtomicP2P
from atomic_p2p.local_monitor import LocalMonitor
from atomic_p2p.utils.logging import getLogger


def min_length(data):
    if len(data) % 16 != 0:
        return data + " " * (16 - len(data) % 16)
    else:
        return data


parser = ArgumentParser()
parser.add_argument("address", help="Service's host address.")
parser.add_argument("-t", "--target", default="127.0.0.1:8000",
                    help="A peer address in Net.", dest="target")
parser.add_argument("-c", "--cert", default="data/atomic_p2p.pem",
                    help="Cert file path.", dest="cert")
parser.add_argument("-as", "--auto-start", action="store_true",
                    default=False, help="Auto start whole service.")
parser.add_argument("-ajn", "--auto-join-net", action="store_true",
                    default=False, help="Auto join a with Net address")
parser.add_argument("-lmp", "--local-monitor-pass",
                    dest="local_monitor_pass", default=None, type=min_length,
                    help="Allow local monitor conntect")

args, left = parser.parse_known_args()

role = "core"
address = args.address
target = args.target
name = "core"
cert = args.cert
auto_start = args.auto_start
auto_join_net = args.auto_join_net
local_monitor_pass = args.local_monitor_pass
    
logger = getLogger(name="AtomicP2P", add_monitor_pass=local_monitor_pass)
atomic_p2p = AtomicP2P(
    role=role, addr=address, name=name, cert=cert, logger=logger)

if local_monitor_pass is not None:
    local_monitor = LocalMonitor(
        service=atomic_p2p, password=local_monitor_pass, logger=logger)
    atomic_p2p.services["local_monitor"] = local_monitor

if auto_start is True:
    atomic_p2p.start()
if auto_join_net is True and target is not None:
    if auto_start is False:
        atomic_p2p.start()
    atomic_p2p._on_command(["peer", "join", target])

