import pytest

from LibreCisco.utils.message import Message, Handler


@pytest.fixture(scope='class')
def message(default_peer, self_hash):
    return Message(_to=('0.0.0.0', 9000), _from=default_peer.host,
                   _hash=self_hash, _type='a', _data='test text')


@pytest.fixture(scope='class')
def handler():
    return Handler(None)
