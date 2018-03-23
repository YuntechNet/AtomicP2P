from queue import Queue

from utils.Task import Task
from utils.LibCisco import LibCisco

class TestLibCisco:

    def test_init(self):
        core = LibCisco(Queue())
        assert hasattr(core, 'outputQueue') == True
        assert core.redisManager.isExit() == False
        core.exit()
        assert core.redisManager.isExit() == True

    def test_command(self):
        core = LibCisco(Queue())
        core.command(Task('A', 'B', 'TestContent'))
        core.exit()
        assert core.redisManager.isExit() == True
        assert core.isExit() == True

