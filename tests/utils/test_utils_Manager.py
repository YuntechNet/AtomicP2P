import pytest
from queue import Queue

from utils.Manager import Manager, ThreadManager, ProcessManager

class TestManager:

    def test_init(self):
        m = Manager('NAME', Queue())
        assert m.name == 'NAME'
        assert m.outputQueue.qsize() == 1

    def test_print(self):
        m = Manager('NAME', Queue())
        assert m.name == 'NAME'
        assert m.outputQueue.qsize() == 1
        m.print('test')
        assert m.outputQueue.qsize() == 2

class TestThreadManager:

    def test_init(self):
        m = ThreadManager('NAME', Queue())
        assert m.stopped.isSet() == False

    @pytest.mark.skip('L24:Seaking mock.')
    def test_start(self):
        m = ThreadManager('NAME', Queue())

    def test_exit(self):
        m = ThreadManager('NAME', Queue())
        assert m.isExit() == False
        m.exit()
        assert m.isExit() == True

    def test_isExit(self):
        m = ThreadManager('NAME', Queue())
        assert m.stopped.isSet() == False
        m.exit()
        assert m.stopped.isSet() == True
        
class TestProcessManager:

    def test_init(self):
        m = ProcessManager('NAME', Queue())
        assert m.stopped.is_set() == False
        assert m.mainProcessCallback == None

    @pytest.mark.skip('L42:Seaking mock.')
    def test_start(self):
        m = ProcessManager('NAME', Queue())

    def test_exit(self):
        m = ProcessManager('NAME', Queue())
        assert m.isExit() == False
        m.exit()
        assert m.isExit() == True

    def test_isExit(self):
        m = ProcessManager('NAME', Queue())
        assert m.stopped.is_set() == False
        m.exit()
        assert m.stopped.is_set() == True
        
