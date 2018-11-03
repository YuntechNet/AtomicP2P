import pytest

from LibreCisco.peer.peer_info import PeerInfo


@pytest.fixture(scope='session')
def peer_info():
    pi = PeerInfo(name='name', role='role', host=('0.0.0.0', 9000))
    return pi


@pytest.fixture(scope='session')
def peer_info2():
    pi = PeerInfo(name='name2', role='role', host=('0.0.0.0', 9001))
    return pi
