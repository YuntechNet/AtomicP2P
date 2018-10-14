import time
import pytest
from peer import Peer

@pytest.yield_fixture(scope='module')
def core1():
    core = Peer(role='core', name='core01', host=('0.0.0.0', 8000))
    core.start()
    yield core
    core.stop()

@pytest.yield_fixture(scope='module')
def switch1():
    switch = Peer(role='sw', name='switch01', host=('0.0.0.0', 8010))
    switch.start()
    yield switch
    switch.stop()

@pytest.yield_fixture(scope='module')
def switch2():
    switch = Peer(role='sw', name='switch02', host=('0.0.0.0', 8011))
    switch.start()
    yield switch
    switch.stop()

@pytest.fixture(scope='module')
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

