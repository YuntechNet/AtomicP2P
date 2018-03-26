import pytest
from queue import Queue

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
        iS = InputStream(Queue())
        assert iS.outputQueue.qsize() == 2

    def test_mainProcessCallback(self):
        iS = InputStream(Queue())
        iS.instance = { 'inputStream': iS }
        iS.mainProcessCallback('exit')
        assert iS.isExit() == True

    @pytest.mark.skip('L41-45:Seaking mock.')
    def test_run(sefl):
        pass

    def test_execute(self):
        iS = InputStream(Queue())
        iS.instance = { 'inputStream': iS }
        #iS.execute('--libcisco')
        #iS.execute('--switch')
        #iS.execute('--schedule')
        #iS.execute('--libserver')
        iS.execute('exit')
        assert iS.isExit() == True
