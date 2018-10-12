import pytest

from peer.peer_info import PeerInfo
from peer.message import Message

@pytest.fixture(scope='class')
def peer_info():
    pi = PeerInfo(name='name', role='role', host=('0.0.0.0', 9000))
    return pi
    

@pytest.fixture(scope='class')
def message():
    m = Message(_ip=('0.0.0.0', 9000), _type='a', _data='test text')
    return m

