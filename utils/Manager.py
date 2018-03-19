import time, threading, queue
from multiprocessing import Process
from multiprocessing import Event as ProcessEvent
from multiprocessing.managers import BaseManager
from utils.Enums import LogLevel

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
        BaseManager.__init__(self)
        Manager.__init__(self, name, outputQueue)
        self.stopped = ProcessEvent()
        #self.redis = RedisManager(name)

    def exit(self):
        self.print('stop singal recieved & set. PID: %s' % str(self.pid))
        self.stopped.set()

    def isExit(self):
        return self.stopped.is_set()
