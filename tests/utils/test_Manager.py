from queue import Queue
from utils.Manager import Manager

class TestManager:

    def test_init(self):
        manager = Manager('Test', Queue())
        assert manager.name == 'Test'
        assert manager.outputQueue.qsize() == 1
