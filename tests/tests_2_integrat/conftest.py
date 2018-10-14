import os
import time
import pytest
from LibreCisco.peer import Peer
from LibreCisco.utils.create_x509_cert import create_self_signed_cert

@pytest.fixture(scope='session')
def cert():
    return create_self_signed_cert(os.getcwd(), 'data/test.pem', 'data/test.key')

@pytest.yield_fixture(scope='session')
def core1(cert):
    core = Peer(role='core', name='core01', host=('0.0.0.0', 8000), cert=cert)
    core.start()
    yield core
    core.stop()

@pytest.yield_fixture(scope='session')
def switch1(cert):
    switch = Peer(role='sw', name='switch01', host=('0.0.0.0', 8010), cert=cert)
    switch.start()
    yield switch
    switch.stop()

@pytest.yield_fixture(scope='session')
def switch2(cert):
    switch = Peer(role='sw', name='switch02', host=('0.0.0.0', 8011), cert=cert)
    switch.start()
    yield switch
    switch.stop()

@pytest.fixture(scope='session')
def node(core1, switch1, switch2):
    nodes = {
        'core_1': core1,
        'sw_1': switch1,
        'sw_2': switch2
    }

    nodes['sw_1'].sendMessage(('127.0.0.1', 8000), 'join')
    nodes['sw_2'].sendMessage(('127.0.0.1', 8000), 'join')

    time.sleep(2)
    return nodes

