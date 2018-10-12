import pytest
from peer import Peer
from peer.message import Message

@pytest.fixture(scope='class')
def message():
    m = Message(_ip=('0.0.0.0', 9000), _type='a', _data='test text')
    return m

@pytest.fixture(scope='module')
def default_peer():
    return Peer()

