import os
from os import getcwd
from os.path import join
import time
import pytest

from LibreCisco.peer import Peer
from LibreCisco.peer.communication.net import JoinHandler
from LibreCisco.utils.security import self_hash as sh, create_self_signed_cert


@pytest.fixture(scope='session')
def self_hash():
    return sh(join(os.getcwd(), 'LibreCisco'))


@pytest.fixture(scope='session')
def cert():
    return create_self_signed_cert(getcwd(), 'data/test.pem', 'data/test.key')


@pytest.yield_fixture(scope='function')
def malware_peer(cert):
    malware_hash = sh(join(getcwd(), 'LibreCisco', 'peer'))
    mp = Peer(role='sw', name='switch_malware', host=('127.0.0.1', 8012),
              cert=cert, _hash=malware_hash)
    mp.start()
    yield mp
    mp.stop()
    time.sleep(1)


@pytest.yield_fixture(scope='function')
def core1(cert, self_hash):
    core = Peer(role='core', name='core01',
                host=('127.0.0.1', 8000), cert=cert, _hash=self_hash)
    core.start()
    yield core
    core.stop()
    time.sleep(1)


@pytest.yield_fixture(scope='function')
def switch1(cert, self_hash):
    switch = Peer(role='sw', name='switch01',
                  host=('127.0.0.1', 8010), cert=cert, _hash=self_hash)
    switch.start()
    yield switch
    switch.stop()
    time.sleep(1)


@pytest.yield_fixture(scope='function')
def switch2(cert, self_hash):
    switch = Peer(role='sw', name='switch02',
                  host=('127.0.0.1', 8011), cert=cert, _hash=self_hash)
    switch.start()
    yield switch
    switch.stop()
    time.sleep(1)


@pytest.fixture(scope='session')
def net(core1, switch1, switch2):
    nodes = {
        'core_1': core1,
        'sw_1': switch1,
        'sw_2': switch2
    }

    nodes['sw_1'].handler_unicast_packet(('127.0.0.1', 8000), JoinHandler.pkt_type)
    nodes['sw_2'].handler_unicast_packet(('127.0.0.1', 8000), JoinHandler.pkt_type)

    time.sleep(8)
    return nodes
