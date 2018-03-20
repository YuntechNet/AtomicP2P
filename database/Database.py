import sqlite3, time

from utils.Enums import LogLevel
from utils.Manager import Manager

# TempDatabase
#   Class definition of local database which store connection data.
#   Include serveral method to access db data like:
#     Temporary store of remote switch info, schedules.
#
class TempDatabase(Manager):
    
    def __init__(self, outputQueue, config):
        Manager.__init__(self, 'TempDatabase', outputQueue)
        self.conn = sqlite3.connect(config['path'], check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor = self.cursor.execute('CREATE TABLE IF NOT EXISTS Switch(IPv4 TEXT PRIMARY KEY, content TEXT);')
        self.cursor = self.cursor.execute('CREATE TABLE IF NOT EXISTS Schedule(Name TEXT PRIMARY KEY, content TEXT);')
        self.conn.commit()
        self.print('Inited.')

    def commit(self):
        self.conn.commit()

    def execute(self, cmd):
        self.cursor = self.cursor.execute(cmd)
        self.commit()
        return self.cursor

    def close(self):
        self.conn.close()

    def commitClose(self):
        self.conn.commit()
        self.close()

# RemoteDatabase
#   Class definition of remote database which sotre connection data.
#   Include serveral method to access db data like:
#     Switch IP, username, password.
#
class RemoteDatabase(Manager):

    def __init__(self, outputQueue, config):
        Manager.__init__(self, 'RemoteDatabase', outputQueue)
        self.type = config['type']
        self.conn = None
 
        if self.type == 'mongodb':
            from pymongo import MongoClient
            self.conn = MongoClient('%s:%s' % (config['host'], config['port']))
            self.db = self.conn[config['dbName']]
            self.switchCol = self.db[config['switchColName']]
            self.ipCol = self.db[config['ipColName']]
        elif self.type == 'mysql':
            # import pymysql
            self.tabName = config['tabname']
            pass
        else:
            self.print('Cat\'t load database type. must be mongodb or mysql.', LogLevel.ERROR)
        self.print('Inited.')

    def close(self):
        if self.type == 'mongodb':
            self.dbConn.close()
