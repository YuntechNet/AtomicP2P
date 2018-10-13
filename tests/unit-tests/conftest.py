import pytest
from peer import Peer

@pytest.fixture(scope='module')
def default_peer():
    return Peer(host=('0.0.0.0', 8000), name='name', role='role')

