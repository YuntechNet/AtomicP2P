import pytest
from queue import Queue

from Config import Config
from network.Command import Command
from network.Manager import RedisManager

class TestRedisManager:

    @pytest.fixture(scope='session')
    def redis(self):
        r = RedisManager(None, 'Test-Redis', [], Queue(), None)
        return r

    def test_loadConfig(self, mocker, redis):
        assert redis.loadConfig(config=Config) == True
        assert redis.loadConfig(config={}) == False

    @pytest.mark.skip('L36-45:Seaking mock.')
    def test_run(self, redis):
        pass

    @pytest.mark.skip('L48:Seaking mock.')
    def test_pub(self, redis):
        pass

    def test_isMine(self, redis):
        assert redis.isMine(Command('A', 'Test-Redis', 'Test')) == True
        assert redis.isMine(Command('A', 'B', 'Test')) == False

    def test_exit(self, mocker, redis):
        redis.exit()
        assert redis.stopped.isSet() == True
