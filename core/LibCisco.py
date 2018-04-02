
from Config import Config
from utils.Manager import ProcessManager
from utils.Enums import LogLevel

class LibCisco(ProcessManager):

    def __init__(self, outputQueue, argv=None, sleep=0, config=Config):
        ProcessManager.__init__(self, 'LibCisco', outputQueue)
        self.sleep = sleep

        if not self.loadConfig(config) or self.isExit():
            self.stopped.set()
            return
        self.print('Inited', LogLevel.SUCCESS)

    def start(self, instance):
        self.instance = instance
        super(LibCisco, self).start()

    def loadConfig(self, config=Config):
        self.print('Loading config')
        if hasattr(config, 'LIB_CISCO'):
            self.print('Config loaded.')
            return True
        else:
            self.print('Config must contain LIB_CISCO attribute.', LogLevel.ERROR)
            return False
    
    def exit(self):
        super(LibCisco, self).exit()

