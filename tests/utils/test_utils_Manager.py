from queue import Queue

from communicate.Manager import RedisManager
from communicate.Command import Command
from utils.Manager import Manager, ThreadManager, ProcessManager

class TestManager:

    def test_init(self):
        manager = Manager('Test', Queue())
        assert manager.name == 'Test'
        assert manager.outputQueue.qsize() == 1

    def test_print(self):
        manager = Manager('Test', Queue())
        manager.print('123')
        assert manager.outputQueue.qsize() == 2

    def test_command(self):
        manager = Manager('Test', Queue())
        #manager.command('command')
        pass

class TestThreadManager:

    def test_init(self):
        thread = ThreadManager('Test', Queue())
        assert thread.stopped.isSet() == False

    def test_exit(self):
        thread = ThreadManager('Test', Queue())
        assert thread.stopped.isSet() == False
        thread.exit()
        assert thread.stopped.isSet() == True
        assert thread.outputQueue.qsize() == 2

    def test_isExit(self):
        thread = ThreadManager('Test', Queue())
        assert thread.isExit() == False
        thread.exit()
        assert thread.isExit() == True

class TestProcessManager:

    def test_init(self):
        process = ProcessManager('Test', Queue())
        assert process.stopped.is_set() == False
        assert process.mainProcessCallback == None

    def test_exit(self):
        process = ProcessManager('Test', Queue())
        assert process.stopped.is_set() == False
        process.exit()
        assert process.stopped.is_set() == True
        assert process.outputQueue.qsize() == 2

    def test_isExit(self):
        process = ProcessManager('Test', Queue())
        assert process.isExit() == False
        process.exit()
        assert process.isExit() == True

    def callbackForTestCommand(self, command):
        assert command == 'exit'

    def command(self):
        process = ProcessManager('Test', Queue(), self.callbackForTestCommand)
        process.redis = RedisManager('Test-Redis', [], Queue(), None)
        assert process.command(Command('A', 'B', 'TestContent')) == False
        assert process.command(Command('A', 'Test-Redis', 'online-signal')) == True
        assert process.command(Command('A', 'Test-Redis', 'heart-beat')) == True
        assert process.command(Command('A', 'Test-Redis', 'heart-beat-response')) == True
        assert process.command(Command('A', 'Test-Redis', 'shutdown')) == True
        assert process.command(Command('A', 'Test-Redis', '(else indent)')) == False
