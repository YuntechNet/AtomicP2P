import os, time

from network.Command import Command, Commander
from utils.Manager import ThreadManager
from utils.Enums import LogLevel, CommandType

class OutputStream(ThreadManager):

    def __init__(self, inputStream, outputQueue):
        ThreadManager.__init__(self, 'OutputStream', outputQueue)
        self.inputStream = inputStream
        self.print('Inited.', LogLevel.SUCCESS)

    def run(self):
        while not self.stopped.wait(0.1) or not self.outputQueue.empty():
            if not self.outputQueue.empty():
                print('[%17f]%s %s\x1b[0m' % (self.outputQueue.get()))
            elif self.inputStream.isExit():
                self.exit()
        os.system('kill %d' % os.getpid())

    def exit(self):
        super(OutputStream, self).exit()
        self.outputQueue.put((time.time(), LogLevel.SUCCESS.value, 'LibCisco all Process/Thread exited, bye.'))

class InputStream(ThreadManager):
    
    def __init__(self, outputQueue, redis):
        ThreadManager.__init__(self, 'InputStream', outputQueue)
        self.outputQueue = outputQueue
        self.redis = redis
        self.print('Inited.', LogLevel.SUCCESS)

    def run(self):
        while not self.isExit():
            if self.outputQueue.empty():
                choice = input('> ')
                self.print('operator execute command: %s' % choice)
                self.execute(choice)

    def execute(self, choice):
        if '--libcisco' in choice:
            Commander.processReq(self.redis, 'LibCisco-Redis', choice, None, Command(self.redis.name, 'LibCisco-Redis', choice))
        elif '--switch' in choice:
            Commander.processReq(self.redis, 'SwitchManager-Redis', choice, None, Command(self.redis.name, 'SwitchManager-Redis', choice))
        elif '--schedule' in choice:
            Commander.processReq(self.redis, 'ScheduleManager-Redis', choice, None, Command(self.redis.name, 'ScheduleManager-Redis', choice))
        elif '--libserver' in choice:
            Commander.processReq(self.redis, 'LibServer-Redis', choice, None, Command(self.redis.name, 'LibServer-Redis', choice))
        elif choice == 'exit':
            for (key, values) in self.instance.items():
                values.exit()

