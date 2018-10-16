import os
from os import getcwd
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
    return create_self_signed_cert(getcwd(), 'data/test.pem', 'data/test.key')


@pytest.yield_fixture(scope='session')
def malware_peer(cert):
    malware_hash = sh(join(getcwd(), 'LibreCisco', 'peer'))
    mp = Peer(role='sw', name='switch_malware', host=('0.0.0.0', 8012),
              cert=cert, _hash=malware_hash)
    mp.start()
    yield mp
    mp.stop()


@pytest.yield_fixture(scope='session')
def core1(cert, self_hash):
    core = Peer(role='core', name='core01',
                host=('0.0.0.0', 8000), cert=cert, _hash=self_hash)
    core.start()
    yield core
    core.stop()


@pytest.yield_fixture(scope='session')
def switch1(cert, self_hash):
    switch = Peer(role='sw', name='switch01',
                  host=('0.0.0.0', 8010), cert=cert, _hash=self_hash)
    switch.start()
    yield switch
    switch.stop()


@pytest.yield_fixture(scope='session')
def switch2(cert, self_hash):
    switch = Peer(role='sw', name='switch02',
                  host=('0.0.0.0', 8011), cert=cert, _hash=self_hash)
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
