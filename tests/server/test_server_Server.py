import pytest, socket

from queue import Queue

from server.Server import LibServer

class TestLibServer:
    
    def test_init(self):
        with pytest.raises(OverflowError):
            s = LibServer(Queue(), ['--LIB_HOST=255.255.255.255', '--LIB_PORT=65536'])
        s = LibServer(Queue())
        s.exit()
        assert s.isExit() == True
