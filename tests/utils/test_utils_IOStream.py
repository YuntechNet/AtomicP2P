import pytest

from queue import Queue

from communicate.Manager import RedisManager
from utils.IOStream import InputStream, OutputStream


class TestInputStream:

    def callbackForMainProcessCallback(self):
        pass

    def test_init(self):
        iStream = InputStream(Queue())        
        iStream.instance = { 'inputStream': iStream }
        iStream.redis = RedisManager('Test', [], Queue(), self.callbackForMainProcessCallback)     
        assert hasattr(iStream, 'outputQueue') == True
        self.mainProcessCallback(iStream)

    @pytest.mark.skip(reason='run loop can\'t be exit.')
    def run(self):
        pass

    def mainProcessCallback(self, iStream):
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
        self.exit(oStream)

    @pytest.mark.skip(reason='run loop can\'t be exit.')
    def run(self):
        pass

    def exit(self, oStream):
        oStream.exit()
        assert oStream.isExit() == True
        
