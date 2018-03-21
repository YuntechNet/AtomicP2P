import time, threading, queue
from multiprocessing import Process
from multiprocessing import Event as ProcessEvent
from utils.Enums import LogLevel
from utils.Task import Task

class Manager:

    def __init__(self, name, outputQueue):
        self.name = name
        self.outputQueue = outputQueue
        self.print('Initing')

    def print(self, msg, level=LogLevel.INFO):
        self.outputQueue.put((time.time(), level.value, '[%s] %s' % (self.name, msg)))

    def command(self, command):
        pass

class ThreadManager(threading.Thread, Manager):
    
    def __init__(self, name, outputQueue):
        threading.Thread.__init__(self)
        Manager.__init__(self, name, outputQueue)
        self.stopped = threading.Event()

    def exit(self):
        self.stopped.set()
        self.print('stop singal recieved & set.')

    def isExit(self):
        return self.stopped.isSet()

class ProcessManager(Process, Manager):

    def __init__(self, name, outputQueue):
        Process.__init__(self)
        Manager.__init__(self, name, outputQueue)
        self.stopped = ProcessEvent()

    def exit(self):
        self.print('stop singal recieved & set. PID: %s' % str(self.pid))
        self.stopped.set()

    def isExit(self):
        return self.stopped.is_set()
    
    def command(self, command):
        if self.redisManager.name == command._to:
            if 'heart-beat' == command._content:
                self.redisManager.pub(command._from, Task(self.redisManager.name, command._from, 'heart-beat-response').to())
                self.redisManager.print('Heart beat from: %s, to: %s, and responsed.' % (command._from, command._to))
            elif 'heart-beat-response' == command._content:
                self.redisManager.print('Heart beat response from: %s, he is good and alive.' % command._from)
            else:
                return False
            return True
        return False
