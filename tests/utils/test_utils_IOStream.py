import pytest
from queue import Queue

from network.Manager import RedisManager
from utils.IOStream import OutputStream, InputStream

class TestOutputStream:

    def test_init(self):
        oS = OutputStream(None, Queue())
        assert oS.inputStream == None
        assert oS.outputQueue.qsize() == 2

    @pytest.mark.skip('L19-24:Seaking mock.')
    def test_run(self):
        pass

    def test_exit(self):
        oS = OutputStream(None, Queue())
        assert oS.isExit() == False
        oS.exit()
        assert oS.isExit() == True

class TestInputStream:

    def test_init(self):
        queue = Queue()
        redis = RedisManager('Test', ['Test'], queue)
        iS = InputStream(queue, redis)
        assert iS.outputQueue.qsize() == 7

    @pytest.mark.skip('L41-45:Seaking mock.')
    def test_run(sefl):
        pass

    def test_execute(self):
        queue = Queue()
        redis = RedisManager('Test', ['Test'], queue)
        iS = InputStream(queue, redis)
        iS.instance = { 'inputStream': iS }
        #iS.execute('--libcisco')
        #iS.execute('--switch')
        #iS.execute('--schedule')
        #iS.execute('--libserver')
        iS.execute('exit')
        assert iS.isExit() == True
