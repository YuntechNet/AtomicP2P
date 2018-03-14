import time, threading, multiprocessing

class Manager:

    def __init__(self, name, outputQueue):
        self.name = name
        self.outputQueue = outputQueue
        self.print('Initing')

    def print(self, msg):
        self.outputQueue.put((time.time(), '[%s] %s' % (self.name, msg)))

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

class ProcessManager(multiprocessing.Process, Manager):

    def __init__(self, name, outputQueue):
        multiprocessing.Process.__init__(self)
        Manager.__init__(self, name, outputQueue)
        self.stopped = multiprocessing.Event()

    def exit(self):
        self.stopped.set()
        self.print('stop singal recieved & set. PID: %s' % str(self.pid))

    def isExit(self):
        return self.stopped.is_set()
