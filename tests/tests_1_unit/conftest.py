import os
import time
import pytest

from LibreCisco.peer import Peer
from LibreCisco.utils.create_x509_cert import create_self_signed_cert

@pytest.fixture(scope='session')
def cert():
    return create_self_signed_cert(os.getcwd(), 'data/test.pem', 'data/test.key')

@pytest.yield_fixture(scope='module')
def default_peer(cert):
    p = Peer(host=('0.0.0.0', 8000), name='name', role='role', cert=cert)
    p.start()

    yield p
    time.sleep(1)
    p.stop()

