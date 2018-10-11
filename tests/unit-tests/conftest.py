import pytest
from peer import Peer

@pytest.fixture(scope='module')
def default_peer():
    return Peer()

