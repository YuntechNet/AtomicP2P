import os
from os.path import join
import time
import pytest

from LibreCisco.peer import Peer
from LibreCisco.utils.security import self_hash as sh, create_self_signed_cert

@pytest.fixture(scope='session')
def self_hash():
    return sh(join(os.getcwd(), 'LibreCisco'))

@pytest.fixture(scope='session')
def cert():
    return create_self_signed_cert(os.getcwd(), 'data/test.pem', 'data/test.key')

@pytest.yield_fixture(scope='module')
def default_peer(cert, self_hash):
    p = Peer(host=('0.0.0.0', 8000), name='name', role='role', cert=cert, _hash=self_hash)
    p.start()

    yield p
    time.sleep(1)
    p.stop()

