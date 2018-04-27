import pytest, os, sqlite3

from queue import Queue

from Config import Config
from database.Database import TempDatabase, RemoteDatabase

class TestTempDatabase:
    
    def test_init(self):
        with pytest.raises(KeyError):
            database = TempDatabase(Queue(), config={})
        config = {'path': './temp.sqlite'}
        database = TempDatabase(Queue(), config=config)
        assert hasattr(database, 'conn') == True
        assert hasattr(database, 'cursor') == True

    def test_commit(self):
        pass

    def test_execute(self):
        config = {'path': './temp_unit_test.sqlite'}
        database = TempDatabase(Queue(), config=config)
        assert database.execute('SELECT * FROM `Switch`').fetchall() == []
        assert database.execute('SELECT * FROM `Schedule`').fetchall() == []
        os.remove('./temp_unit_test.sqlite')

    def test_close(self):
        pass

    def test_commitClose(self):
        config = {'path': './temp_unit_test.sqlite'}
        database = TempDatabase(Queue(), config=config)
        database.commitClose()
        with pytest.raises(sqlite3.ProgrammingError):
            database.execute('SELECT * FROM `Switch`')
        os.remove('./temp_unit_test.sqlite')

class TestRemoteDatabase:

    def test_init(self):
        with pytest.raises(KeyError):
            database = RemoteDatabase(Queue(), config={})
        config = {'type': 'mongodb', 'uri': 'mongodb://libcisco:libcisco@ds155130.mlab.com:55130/libcisco-testmongo', 'dbName': 'libcisco-testmongo', 'switchColName': 'switch', 'ipColName': 'ip'}
        database = RemoteDatabase(Queue(), config=config)
        assert self.hasAttr(database) == True
        database.close()
        assert self.hasAttr(database) == False

        config = {'type': 'mysql'}
        database = RemoteDatabase(Queue(), config=config)
        assert self.hasAttr(database) == False

        config = {'type': 'none'}
        database = RemoteDatabase(Queue(), config=config)
        assert self.hasAttr(database) == False

    def hasAttr(self, database):
        if not hasattr(database, 'conn') or not hasattr(database, 'db') or not hasattr(database, 'switchCol') or not hasattr(database, 'ipCol'):
            return False
        else:
            return True

    def test_close(self):
        pass
