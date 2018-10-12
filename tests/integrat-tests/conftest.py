import time
import pytest
from peer import Peer

@pytest.yield_fixture(scope='module')
def node():
    nodes = {
        'core_1': Peer(role='core', name='core01', ip='0.0.0.0', port=8000),
        'sw_1': Peer(role='sw', name='switch01', ip='0.0.0.0', port=8010),
        'sw_2': Peer(role='sw', name='switch02', ip='0.0.0.0', port=8011)
    }
    for (key, value) in nodes.items():
        value.start()

    nodes['sw_1'].sendMessage(('127.0.0.1', 8000), 'join')
    nodes['sw_2'].sendMessage(('127.0.0.1', 8000), 'join')

    time.sleep(5)
    yield nodes

    for (key, value) in nodes.items():
        value.stop()
