import pytest

from LibreCisco.peer.peer_info import PeerInfo

@pytest.fixture(scope='class')
def peer_info():
    pi = PeerInfo(name='name', role='role', host=('0.0.0.0', 9000))
    return pi
    
