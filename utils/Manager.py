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

    def start(self):
        super(ThreadManager, self).start()

    def exit(self):
        self.stopped.set()
        self.print('stop signal recieved & set.')

    def isExit(self):
        return self.stopped.isSet()

class ProcessManager(Process, Manager):

    def __init__(self, name, outputQueue, callback=None):
        Process.__init__(self)
        Manager.__init__(self, name, outputQueue)
        self.stopped = ProcessEvent()
        self.mainProcessCallback = callback

    def exit(self):
        self.stopped.set()
        self.print('stop signal recieved & set. PID: %s' % str(self.pid))

    def isExit(self):
        return self.stopped.is_set()
    
    def command(self, command):
        if self.redisManager.name == command._to:
            if 'online-signal' == command._content:
                self.redisManager.print('Online signal from %s, he is cool.' % command._from)
            elif 'heart-beat' == command._content:
                self.redisManager.pub(self.redisManager.name, command._from, 'heart-beat-response')
                self.redisManager.print('Heart beat from: %s, to: %s, and responsed.' % (command._from, command._to))
            elif 'heart-beat-response' == command._content:
                self.redisManager.print('Heart beat response from: %s, he is good and alive.' % command._from)
            elif 'shutdown' == command._content and self.mainProcessCallback:
                self.print('Recieve shutdown signal from %s, proceeding...' % command._from)
                self.mainProcessCallback('exit')
            else:
                return False
            return True
        return False
