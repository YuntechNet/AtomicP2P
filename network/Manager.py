import logging, redis

from Config import Config
from network.Command import Commander
from network.commands.Command import Command
from utils.Manager import ThreadManager

class RedisManager(ThreadManager):

    def __init__(self, name, subscribeList, outputQueue, sleep=0, config=Config):
        ThreadManager.__init__(self, '%s' % name, outputQueue)
        self.sleep = sleep

        if not self.loadConfig(config) or self.isExit():
            self.stopped.set()
            return 
        self.rcon = redis.StrictRedis(host=self.address[0], port=self.address[1], password=self.password)
        self.ps = self.rcon.pubsub()
        self.ps.subscribe(subscribeList)
        self.print('Subscribing: %s' % str(subscribeList))
        self.print('Inited', logging.INFO)

    def start(self, instance):
        self.instance = instance
        super(RedisManager, self).start()

    def loadConfig(self, config=Config):
        self.print('Loading config.')
        if hasattr(config, 'REDIS_MANAGER'):
            self.config = config.REDIS_MANAGER
            self.address = self.config['ADDRESS']
            self.password = self.config['PASSWORD']
            self.print('Config loaded.')
            return True
        else:
            self.print('Config must contain REDIS_MANAGER attribute.', logging.ERROR)
            return False

    def run(self):
        while not self.stopped.wait(self.sleep):
            for each in self.ps.listen():
                if each['type'] == 'message':
                    Commander.processRes(self, Command.parse(each['data'].decode('utf-8')))
                elif each['type'] == 'subscribe':
                    self.print('Channel %s subscribed, listening count %d.' % (each['channel'].decode('utf-8'), each['data']))
                elif each['type'] == 'unsubscribe':
                    self.print('Channel %s unsubscribed, listening count %d.' % (each['channel'].decode('utf-8'), each['data']))
            if self.isExit():
                self.ps.close()

    def pub(self, _to, value):
        self.rcon.publish(_to, value)

    def exit(self):
        self.ps.unsubscribe()
        super(RedisManager, self).exit()

    def isMine(self, cmd):
        return True if self.name == cmd._to else False

