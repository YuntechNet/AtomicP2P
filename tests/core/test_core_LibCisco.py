from queue import Queue

from network.Command import Command
from core.LibCisco import LibCisco

class TestLibCisco:

    def test_init(self):
        core = LibCisco(Queue())
        assert hasattr(core, 'outputQueue') == True
        core.exit()
        assert core.isExit() == True

    def command(self):
        core = LibCisco(Queue())
        core.command(Command('A', 'B', 'TestContent'))
        core.exit()
        assert core.redis.isExit() == True
        assert core.isExit() == True

