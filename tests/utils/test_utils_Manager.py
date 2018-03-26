from queue import Queue

from communicate.Manager import RedisManager
from communicate.Command import Command
from utils.Manager import Manager, ThreadManager, ProcessManager

class TestManager:

    def test_init(self):
        manager = Manager('Test', Queue())
        assert manager.name == 'Test'
        assert manager.outputQueue.qsize() == 1
        self.print(manager)

    def print(self, manager):
        manager.print('123')
        assert manager.outputQueue.qsize() == 2

class TestThreadManager:

    def test_init(self):
        thread = ThreadManager('Test', Queue())
        assert thread.stopped.isSet() == False
        assert self.isExit(thread) == False
        self.exit(thread)
        assert self.isExit(thread) == True

    def isExit(self, thread):
        return thread.isExit()

    def exit(self, thread):
        assert thread.stopped.isSet() == False
        thread.exit()
        assert thread.stopped.isSet() == True
        assert thread.outputQueue.qsize() == 2


class TestProcessManager:

    def test_init(self):
        process = ProcessManager('Test', Queue())
        assert process.stopped.is_set() == False
        assert process.mainProcessCallback == None
        assert self.isExit(process) == False
        self.exit(process)
        assert self.isExit(process) == True

    def isExit(self, process):
        return process.isExit()

    def exit(self, process):
        assert process.stopped.is_set() == False
        process.exit()
        assert process.stopped.is_set() == True
        assert process.outputQueue.qsize() == 2
