from pytest import fixture

from atomic_p2p.peer.entity import PeerInfo, PeerStatus, PeerRole


@fixture(scope="session")
def peer_info():
    pi = PeerInfo(name="name", role=PeerRole.CORE, host=("0.0.0.0", 9000))
    return pi


@fixture(scope="session")
def peer_info2():
    pi = PeerInfo(name="name2", role=PeerRole.CORE, host=("0.0.0.0", 9001))
    return pi


@fixture(scope="session")
def peer_status():
    return PeerStatus()
