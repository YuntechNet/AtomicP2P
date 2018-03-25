from queue import Queue

from communicate.Command import Command
from core.LibCisco import LibCisco

class TestLibCisco:

    def test_init(self):
        core = LibCisco(Queue())
        assert hasattr(core, 'outputQueue') == True
        assert core.redis.isExit() == False
        core.exit()
        assert core.redis.isExit() == True

    def command(self):
        core = LibCisco(Queue())
        core.command(Command('A', 'B', 'TestContent'))
        core.exit()
        assert core.redis.isExit() == True
        assert core.isExit() == True

