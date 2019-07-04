import pytest

from atomic_p2p.peer.communication import MessageHandler
from atomic_p2p.peer.command import HelpCmd
from atomic_p2p.utils.manager import ProcManager, ThreadManager


@pytest.fixture(scope="module")
def handler(default_peer):
    return MessageHandler(peer=default_peer)


@pytest.fixture(scope="module")
def command(default_peer):
    return HelpCmd(peer=default_peer)


@pytest.fixture(scope="function")
def proc():
    p = ProcManager(auto_register=False)
    p.pkt_handlers["select_handler"] = "handler"
    return p


@pytest.fixture(scope="function")
def thread():
    t = ThreadManager(auto_register=False)
    t.pkt_handlers["select_handler"] = "handler"
    return t
