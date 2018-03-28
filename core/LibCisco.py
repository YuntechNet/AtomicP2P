from utils.Manager import ProcessManager
from core.Command import LibCiscoCommand
from network.Manager import RedisManager
from switch.Manager import SwitchManager

class LibCisco(ProcessManager):

    def __init__(self, outputQueue, argv=None, sleep=0, callback=None):
        ProcessManager.__init__(self, 'LibCisco', outputQueue, callback)
        self.outputQueue = outputQueue
        self.commander = LibCiscoCommand(self)
        self.redis = RedisManager('LibCisco-Redis', ['LibCisco-Redis', 'SwitchManager-Redis', 'ScheduleManager-Redis', 'LibServer-Redis'], outputQueue, self.commander.process)
        

    def start(self):
        self.redis.start()
        super(LibCisco, self).start()
    
    def exit(self):
        self.redis.exit()
        super(LibCisco, self).exit()

