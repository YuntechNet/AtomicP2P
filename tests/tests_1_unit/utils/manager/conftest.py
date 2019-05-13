import pytest
from atomic_p2p.utils.manager import ProcManager, ThreadManager


@pytest.fixture(scope='session')
def proc():
    return ProcManager(auto_register=False)


@pytest.fixture(scope='session')
def thread():
    return ThreadManager(auto_register=False)
