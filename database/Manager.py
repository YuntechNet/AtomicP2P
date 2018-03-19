import threading, redis
from threading import Event

from Config import Config
from utils.Manager import ThreadManager
from database.Database import RemoteDatabase
from utils.Enums import LogLevel

# RemoteDBManager
#   A thread in SwitchManager for communicate with local database.
#
class RemoteDBManager(ThreadManager):

    def __init__(self, outputQueue, tempDB, config, sleep=300):
        ThreadManager.__init__(self, 'RemoteDBManager', outputQueue)
        self.sleep = sleep

        self.tempDB = tempDB
        self.remoteDB = RemoteDatabase(self.outputQueue, config)

    def run(self): # Override
        while not self.stopped.wait(self.sleep):
            self.syncToLocal()

    def syncToLocal(self):
        self.print('Loading devices.')
        if self.remoteDB.type == 'mongodb':
            from bson.json_util import dumps as bsonDumps
            every = self.remoteDB.switchCol.find({})
            for doc in every:
                ip = self.remoteDB.ipCol.find_one({ '_id': doc['ipId'] })
                cmd = 'REPLACE INTO Switch(IPv4, content) VALUES (\'%s\', \'%s\');' % (ip['ipv4'], bsonDumps(doc))
                self.tempDB.execute(cmd)
            self.tempDB.commit()
        elif self.remoteDB.type == 'mysql':
            pass

class RedisManager(ThreadManager):

    def __init__(self, name, subscribeList, outputQueue, sleep=0):
        ThreadManager.__init__(self, '(Redis)%s' % name, outputQueue)
        self.sleep = sleep

        if not self.loadConfig() or self.isExit():
            self.stopped.set()
        self.rcon = redis.StrictRedis(host=self.address[0], port=self.address[1])
        self.ps = self.rcon.pubsub()
        self.ps.subscribe(subscribeList)
        self.print('Subscribing: %s' % str(subscribeList))
        self.print('Inited', LogLevel.SUCCESS)

    def loadConfig(self):
        self.print('Loading config')
        if hasattr(Config, 'REDIS_SERVER'):
            self.config = Config.REDIS_SERVER
            self.address = self.config['ADDRESS']
            return True
        else:
            self.print('Config must contain REDIS_SERVER attribute.', LogLevel.ERROR)
            return False

    def run(self):
        while not self.stopped.wait(self.sleep):
            for each in self.ps.listen():
                if each['type'] == 'message':
                    self.print(each)
                elif each['type'] == 'subscribe':
                    self.print('Channel %s subscirbe %s' % (each['channel'].decode('utf-8'), 'SUCCES' if each['data'] == 1 else 'FAILED'), LogLevel.SUCCESS if each['data'] == 1 else LogLevel.WARNING)
                elif each['type'] == 'unsubscribe':
                    self.print('Channel %s unsubscirbe %s' % (each['channel'].decode('utf-8'), 'SUCCES' if each['data'] == 0 else 'FAILED'), LogLevel.SUCCESS if each['data'] == 0 else LogLevel.WARNING)

    def pub(self, key, value):
        self.rcon.publish(key, value)

    def exit(self):
        self.ps.unsubscribe()
        super(RedisManager, self).exit()
