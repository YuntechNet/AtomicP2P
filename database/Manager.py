import threading, redis
from threading import Event

from Config import Config
from utils.Manager import ThreadManager
from database.Database import TempDatabase, RemoteDatabase
from utils.Enums import LogLevel
from utils.Task import Task

# DatabaseManager
#   A thread in each manager for communication with local and remote database.
#
class DatabaseManager(ThreadManager):

    def __init__(self, outputQueue, config, sleep=300):
        ThreadManager.__init__(self, 'DatabaseManager', outputQueue)
        self.sleep = sleep

        if 'TEMP_DATABASE' in config:
            self.temporDB = TempDatabase(outputQueue, config['TEMP_DATABASE'])
        if 'DATABASE' in config:
            self.remoteDB = RemoteDatabase(outputQueue, config['DATABASE'])
        self.print('inited.', LogLevel.SUCCESS)

    def run(self):
        while not self.stopped.wait(self.sleep):
            self.syncToLocal()

    def sync(self):
        raise NotImplementedError
       
class RedisManager(ThreadManager):

    def __init__(self, name, subscribeList, outputQueue, cmdCallback, sleep=0, config=Config):
        ThreadManager.__init__(self, '%s' % name, outputQueue)
        self.sleep = sleep
        self.cmdCallback = cmdCallback

        if not self.loadConfig(config) or self.isExit():
            self.stopped.set()
            return 
        self.rcon = redis.StrictRedis(host=self.address[0], port=self.address[1], password=self.password)
        self.ps = self.rcon.pubsub()
        self.ps.subscribe(subscribeList)
        self.print('Subscribing: %s' % str(subscribeList))
        self.print('Inited', LogLevel.SUCCESS)

    def loadConfig(self, config):
        self.print('Loading config.')
        if hasattr(config, 'REDIS_MANAGER'):
            self.config = config.REDIS_MANAGER
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
