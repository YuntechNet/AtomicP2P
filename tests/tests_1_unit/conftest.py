import time
import pytest
from peer import Peer

@pytest.yield_fixture(scope='module')
def default_peer():
    p = Peer(host=('0.0.0.0', 8000), name='name', role='role')
    yield p
    time.sleep(1)
    p.stop()

