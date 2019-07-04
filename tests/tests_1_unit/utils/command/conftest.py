
import pytest
from atomic_p2p.utils.command import Command


@pytest.fixture(scope="class")
def command():
    return Command(None)
