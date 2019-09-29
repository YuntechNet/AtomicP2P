from pytest import fixture

from atomic_p2p.manager import ProcManager, ThreadManager
from atomic_p2p.peer.communication import MessageHandler
from atomic_p2p.peer.command import HelpCmd


@fixture(scope="module")
def handler(default_peer):
    return MessageHandler(peer=default_peer)


@fixture(scope="module")
def command(default_peer):
    return HelpCmd(peer=default_peer)


@fixture(scope="function")
def proc():
    p = ProcManager()
    return p


@fixture(scope="function")
def thread():
    t = ThreadManager()
    return t
