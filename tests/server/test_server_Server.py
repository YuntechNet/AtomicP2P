import pytest, socket

from queue import Queue

from utils.Task import Task
from server.Server import LibServer

class TestLibServer:
    
    def test_init(self):
        with pytest.raises(OverflowError):
            s = LibServer(Queue(), ['--LIB_HOST=255.255.255.255', '--LIB_PORT=65536'])
        s = LibServer(Queue())
        self.command(s)
        s.exit()
        assert s.isExit() == True

    def run(self):
        pass

    def command(self, s):
        s.command(Task('A', 'B', 'TestContent'))
        s.command(Task('A', 'LibServer-Redis', 'TestContent'))
