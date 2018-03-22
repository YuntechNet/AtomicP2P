import threading, redis
from threading import Event

from Config import Config
from utils.Manager import ThreadManager
from database.Database import RemoteDatabase
from utils.Enums import LogLevel
from utils.Task import Task

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

    def __init__(self, name, subscribeList, outputQueue, cmdCallback, sleep=0):
        ThreadManager.__init__(self, '%s' % name, outputQueue)
        self.sleep = sleep
        self.cmdCallback = cmdCallback

        if not self.loadConfig() or self.isExit():
            self.stopped.set()
        self.rcon = redis.StrictRedis(host=self.address[0], port=self.address[1], password=self.password)
        self.ps = self.rcon.pubsub()
        self.ps.subscribe(subscribeList)
        self.print('Subscribing: %s' % str(subscribeList))
        self.print('Inited', LogLevel.SUCCESS)

    def loadConfig(self):
        self.print('Loading config.')
        if hasattr(Config, 'REDIS_MANAGER'):
            self.config = Config.REDIS_MANAGER
            self.address = self.config['ADDRESS']
            self.password = self.config['PASSWORD']
            return True
        else:
            self.print('Config must contain REDIS_MANAGER attribute.', LogLevel.ERROR)
            return False

    def run(self):
        while not self.stopped.wait(self.sleep):
            for each in self.ps.listen():
                if each['type'] == 'message':
                    self.cmdCallback(Task.parse(each['data'].decode('utf-8')))
                elif each['type'] == 'subscribe':
                    self.print('Channel %s subscribed, listening count %d.' % (each['channel'].decode('utf-8'), each['data']))
                elif each['type'] == 'unsubscribe':
                    self.print('Channel %s unsubscribed, listening count %d.' % (each['channel'].decode('utf-8'), each['data']))
            if self.isExit():
                self.ps.close()

    def pub(self, _from, _to, value):
        self.rcon.publish(_to, Task(_from, _to, value).to())

    #def pubAll(self, _from, value):
    #    for each in self.subscribeList:
    #        self.rcon.publish(each, Task(_from, each, value).to())

    def exit(self):
        self.ps.unsubscribe()
        super(RedisManager, self).exit()

    def isMine(self, task):
        return True if self.name == task._to else False
