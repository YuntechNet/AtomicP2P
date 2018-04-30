from queue import Queue

from network.Command import Command
from core.LibreCisco import LibreCisco

class TestLibCisco:

    def test_init(self):
        core = LibreCisco(Queue())
        assert hasattr(core, 'outputQueue') == True
        core.exit()
        assert core.isExit() == True

    def command(self):
        core = LibreCisco(Queue())
        core.command(Command('A', 'B', 'TestContent'))
        core.exit()
        assert core.redis.isExit() == True
        assert core.isExit() == True

