import time

from utils.Task import Task
from utils.Manager import ThreadManager
from utils.Enums import LogLevel

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

    def exit(self):
        super(OutputStream, self).exit()
        self.outputQueue.put((time.time(), LogLevel.SUCCESS.value, 'LibCisco all Process/Thread exited, bye.'))

class InputStream(ThreadManager):
    
    def __init__(self, outputQueue):
        ThreadManager.__init__(self, 'InputStream', outputQueue)
        self.outputQueue = outputQueue
        self.print('Inited.', LogLevel.SUCCESS)

    def mainProcessCallback(self, cmd):
        self.execute(cmd)

    def run(self):
        while not self.isExit():
            if self.outputQueue.empty():
                choice = input('> ')
                self.print('operator execute command: %s' % choice)
                self.execute(choice)

    def execute(self, choice):
        if '--libcisco' in choice:
            self.redis.pub(self.redis.name, 'LibCisco-Redis', choice.replace('--libcisco ', ''))
        elif '--switch' in choice:
            self.redis.pub(self.redis.name, 'SwitchManager-Redis', choice.replace('--switch ', ''))
        elif '--schedule' in choice:
            self.redis.pub(self.redis.name, 'ScheduleManager-Redis', choice.replace('--schedule ', ''))
        elif '--libserver' in choice:
            self.redis.pub(self.redis.name, 'LibServer-Redis', choice.replace('--libserver ', ''))
        elif choice == 'exit':
            for (key, values) in self.instance.items():
                values.exit()

