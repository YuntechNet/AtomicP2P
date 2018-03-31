
from utils.Manager import ProcessManager

class LibCisco(ProcessManager):

    def __init__(self, outputQueue, argv=None, sleep=0):
        ProcessManager.__init__(self, 'LibCisco', outputQueue)
        self.outputQueue = outputQueue

    def start(self, instance):
        self.instance = instance
        super(LibCisco, self).start()
    
    def exit(self):
        super(LibCisco, self).exit()

