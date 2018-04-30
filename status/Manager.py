import logging

from Config import Config
from utils.Manager import ThreadManager
from status.commands.Online import Online

class StatusManager(ThreadManager):

    def __init__(self, outputQueue, argv=[], sleep=300, config=Config):
        ThreadManager.__init__(self, 'StatusManager', outputQueue)
        self.__sleep = sleep
        self.status = {}

        if not self.loadConfig(config=config) or self.isExit():
            self.stopped.set()
            return
        self.loadArgv(argv)
        self.print('Inited.', logging.INFO)

    def start(self, instance):
        self.redis = instance['redisManager']
        super(StatusManager, self).start()

    def loadConfig(self, config=Config):
        self.print('Loading config.', logging.DEBUG)
        if hasattr(config, 'STATUS_MANAGER'):
            self.__config = config.STATUS_MANAGER
            self.print('Config loaded.', logging.DEBUG)
            return True
        else:
            self.print('Config must contain STATUS_MANAGER attribute.', logging.ERROR)
            return False

    def loadArgv(self, argv):
        self.print('Loading argv.', logging.DEBUG)
        self.print('Argv loaded.', logging.DEBUG)

    def run(self):
        while not self.stopped.wait(self.__sleep):
            Online.req(self.redis)

    def markStatus(self, name, value):
        self.status[name] = value

