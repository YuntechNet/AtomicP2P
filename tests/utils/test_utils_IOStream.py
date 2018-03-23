import pytest

from queue import Queue

from database.Manager import RedisManager
from utils.IOStream import InputStream, OutputStream


class TestInputStream:

    def test_init(self):
        iStream = InputStream(Queue())        
        assert hasattr(iStream, 'outputQueue') == True

    @pytest.mark.skip(reason='run loop can\'t be exit.')
    def test_run(self):
        pass

    def callbackForMainProcessCallback(self):
        pass

    def test_mainProcessCallback(self):
        iStream = InputStream(Queue())
        iStream.redis = RedisManager('Test', [], Queue(), self.callbackForMainProcessCallback)     
        iStream.instance = { 'inputStream': iStream }
        iStream.mainProcessCallback('--libcisco') 
        iStream.mainProcessCallback('--switch') 
        iStream.mainProcessCallback('--schedule') 
        iStream.mainProcessCallback('--libserver') 
        iStream.mainProcessCallback('exit')
        assert iStream.isExit() == True 

class TestOutputStream:

    def test_init(self):
        iStream = InputStream(Queue())
        oStream = OutputStream(iStream, Queue())
        assert hasattr(oStream, 'inputStream') == True
        assert hasattr(oStream, 'outputQueue') == True

    @pytest.mark.skip(reason='run loop can\'t be exit.')
    def test_run(self):
        pass

    def test_exit(self):
        iStream = InputStream(Queue())
        oStream = OutputStream(iStream, Queue())
        oStream.exit()
        assert oStream.isExit() == True
        
