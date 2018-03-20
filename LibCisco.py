from utils.Manager import ProcessManager
from database.Manager import RedisManager
from switch.Manager import SwitchManager

class LibCisco(ProcessManager):

    def __init__(self, outputQueue, argv=None, sleep=0):
        ProcessManager.__init__(self, 'LibCisco', outputQueue)
        self.outputQueue = outputQueue
        self.redisManager = RedisManager('LibCisco', ['LibCisco', 'SwitchManager', 'ScheduleManager', 'LibServer'], outputQueue, self.command)
        self.redisManager.start()
    
    def command(self, command):
        if 'heart-beat' in command:
            self.print('Heart Beat: %s' % command)

    def exit(self):
        self.redisManager.exit()
        super(LibCisco, self).exit()

