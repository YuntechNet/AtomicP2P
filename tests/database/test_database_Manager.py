import pytest, os
from queue import Queue

from Config import Config
from database.Database import TempDatabase
from database.Manager import DatabaseManager
from network.Manager import RedisManager
from network.Command import Command

class TestDatabaseManager:

    #def test_init(self):
    def init(self):
        config = {'type': 'mongodb', 'uri': 'mongodb://libcisco:libcisco@ds155130.mlab.com:55130/libcisco-testmongo', 'dbName': 'libcisco-testmongo', 'switchColName': 'switch', 'ipColName': 'ip'}
        database = TempDatabase(Queue(), {'path': './temp_unit_test.sqlite'})
        manager = RemoteDBManager(Queue(), database, config)
        assert self.hasAttr(manager) == True
        os.remove('./temp_unit_test.sqlite')

    def hasAttr(self, manager):
        if not hasattr(manager, 'sleep') or not hasattr(manager, 'tempDB') or not hasattr(manager, 'remoteDB'):
            return False
        else:
            return True

    @pytest.mark.skip(reason='run loop can\'t not be exit')
    def test_run(self):
        pass

    #def test_syncToLocal(self):
    def syncToLocal(self):
        config = {'type': 'mongodb', 'uri': 'mongodb://libcisco:libcisco@ds155130.mlab.com:55130/libcisco-testmongo', 'dbName': 'libcisco-testmongo', 'switchColName': 'switch', 'ipColName': 'ip'}
        database = TempDatabase(Queue(), {'path': './temp_unit_test.sqlite'})
        manager = RemoteDBManager(Queue(), database, config)
        assert self.hasAttr(manager) == True
        manager.syncToLocal()

        config = {'type': 'mysql'}
        manager = RemoteDBManager(Queue(), database, config)
        assert self.hasAttr(manager) == True
        manager.syncToLocal()
        os.remove('./temp_unit_test.sqlite')
        
class TestRedisManager:

    def test_init(self):
        pass

    def test_loadConfig(self):
        redis = RedisManager('Test', [], Queue(), config=None)
        assert redis.isExit() == True
        #assert hasattr(redis, 'rcon') == False
        #assert redis.loadConfig(config={}) == False

    def callbackForIsMine(self, command):
        pass

    def test_isMine(self):
        redis = RedisManager('Test', [], Queue(), self.callbackForIsMine, config=None)
        assert redis.isMine(Command('A', 'B', 'TestContent')) == False
        assert redis.isMine(Command('A', 'Test', 'TestContent')) == True

    def callbackForExit(self):
        pass

    def test_exit(self):
        redis = RedisManager('Test', [], Queue(), self.callbackForExit)
        redis.exit()
        assert redis.isExit() == True

    @pytest.mark.skip(reason='run loop can\'t not be exit')
    def test_run(self):
        pass
