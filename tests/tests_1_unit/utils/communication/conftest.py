import pytest

from LibreCisco.utils.communication import Packet, Handler


@pytest.fixture(scope='class')
def packet(default_peer, self_hash):
    return Packet(dst=('0.0.0.0', 9000), src=default_peer.peer_info.host,
                  _hash=self_hash, _type='a', _data={'test': 'test text'})


@pytest.fixture(scope='class')
def handler(default_peer):
    return Handler(peer=default_peer, pkt_type='test_key')
