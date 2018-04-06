import logging

from Config import Config
from utils.Manager import ThreadManager

class StatusManager(ThreadManager):

    def __init__(self, outputQueue, argv=[], sleep=60, config=Config):
        ThreadManager.__init__(self, 'StatusManager', outputQueue)
        self.sleep = sleep
        self.print('Inited.', logging.INFO)

    def start(self, instance):
        self.instance= instance
        super(StatusManager, self).start()

    def loadConfig(self, config=Config):
        self.print('Loading config')
        if hasattr(config, 'STATUS_MANAGER'):
            self.config = config.STATUS_MANAGER
            self.print('Config loaded.')
            return True
        else:
            self.print('Config must contain STATUS_MANAGER attribute.', logging.ERROR)
            return False

