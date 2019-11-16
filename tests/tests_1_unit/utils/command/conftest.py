
from pytest import fixture

from atomic_p2p.communication.command import Command


@fixture(scope="class")
def command():
    return Command(None)
