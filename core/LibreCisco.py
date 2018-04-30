import logging

from Config import Config
from utils.Manager import ProcessManager

class LibreCisco(ProcessManager):

    def __init__(self, outputQueue, argv=[], sleep=0, config=Config):
        ProcessManager.__init__(self, 'LibreCisco', outputQueue)
        self.sleep = sleep

        if not self.loadConfig(config) or self.isExit():
            self.stopped.set()
            return
        self.print('Inited', logging.INFO)

    def start(self, instance):
        self.instance = instance
        super(LibreCisco, self).start()

    def loadConfig(self, config=Config):
        self.print('Loading config', logging.DEBUG)
        if hasattr(config, 'LIB_CISCO'):
            self.print('Config loaded.', logging.DEBUG)
            return True
        else:
            self.print('Config must contain LIB_CISCO attribute.', logging.ERROR)
            return False
    
    def exit(self):
        super(LibreCisco, self).exit()

