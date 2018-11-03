import pytest
from LibreCisco.peer.monitor.peer_status import PeerStatus


@pytest.fixture(scope='session')
def peer_status(peer_info):
    return PeerStatus(peer_info=peer_info)


@pytest.fixture(scope='session')
def peer_status2(peer_info2):
    return PeerStatus(peer_info=peer_info2)
