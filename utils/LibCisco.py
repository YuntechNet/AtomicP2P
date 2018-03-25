from utils.Manager import ProcessManager
from communicate.Manager import RedisManager
from switch.Manager import SwitchManager

class LibCisco(ProcessManager):

    def __init__(self, outputQueue, argv=None, sleep=0, callback=None):
        ProcessManager.__init__(self, 'LibCisco', outputQueue, callback)
        self.outputQueue = outputQueue
        self.redisManager = RedisManager('LibCisco-Redis', ['LibCisco-Redis', 'SwitchManager-Redis', 'ScheduleManager-Redis', 'LibServer-Redis'], outputQueue, self.command)
        self.redisManager.start()
    
    def command(self, command):
        if super(LibCisco, self).command(command) is False and self.redisManager.name != command._from:
            self.redisManager.print(command.to())

    def exit(self):
        self.redisManager.exit()
        super(LibCisco, self).exit()

