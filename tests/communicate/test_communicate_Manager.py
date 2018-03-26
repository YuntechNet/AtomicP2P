import pytest
from queue import Queue

from Config import Config
from communicate.Command import Command
from communicate.Manager import RedisManager

class TestRedisManager:

    def test_init(self):
        r = RedisManager('Test-Redis', [], Queue(), None)
        assert r.isExit() == False
        r = RedisManager('Test-Redis', [], Queue(), None, config={})
        assert r.isExit() == True

    def test_loadConfig(self):
        r = RedisManager('Test-Redis', [], Queue(), None)
        assert r.loadConfig(config=Config) == True
        assert r.loadConfig(config={}) == False

    @pytest.mark.skip('L36-45:Seaking mock.')
    def test_run(self):
        pass

    @pytest.mark.skip('L48:Seaking mock.')
    def test_pub(self):
        pass

    def test_exit(self):
        r = RedisManager('Test-Redis', [], Queue(), None)
        r.exit()
        assert r.stopped.isSet() == True
        
    def test_isMine(self):
        r = RedisManager('Test-Redis', [], Queue(), None)
        assert r.isMine(Command('A', 'Test-Redis', 'Test')) == True
        assert r.isMine(Command('A', 'B', 'Test')) == False
