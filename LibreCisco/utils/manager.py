from multiprocessing import Process, Event as pEvent
<<<<<<< HEAD
from threading import Thread, Event as tEvent
=======
from multithreading import Thread, Event as tEvent
>>>>>>> Create process/thread base manager


class ProcManager(Process):

<<<<<<< HEAD
    def __init__(self, loopDelay=1, output_field=None, auto_register=False):
=======
    def __init__(self, loopDelay=1, output_field=None):
>>>>>>> Create process/thread base manager
        super(ProcManager, self).__init__()
        self.output_field = output_field
        self.loopDelay = loopDelay
        self.stopped = pEvent()

<<<<<<< HEAD
        if auto_register:
            self.registerHandler()
            self.registerCommand()
=======
        self.registerHandler()
        self.registerCommand()
>>>>>>> Create process/thread base manager

    def registerHandler(self):
        raise NotImplementedError

    def registerCommand(self):
        raise NotImplementedError

    def start(self):
        super(ProcManager, self).start()

    def run(self):
        pass

    def stop(self):
        self.stopped.set()


class ThreadManager(Thread):

<<<<<<< HEAD
    def __init__(self, loopDelay=1, output_field=None, auto_register=False):
=======
    def __init__(self, loopDelay=1, output_field=None):
>>>>>>> Create process/thread base manager
        super(ThreadManager, self).__init__()
        self.output_field = output_field
        self.loopDelay = loopDelay
        self.stopped = tEvent()

<<<<<<< HEAD
        if auto_register:
            self.registerHandler()
            self.registerCommand()
=======
        self.registerHandler()
        self.registerCommand()
>>>>>>> Create process/thread base manager

    def registerHandler(self):
        raise NotImplementedError

    def registerCommand(self):
        raise NotImplementedError

    def start(self):
        super(ThreadManager, self).start()

    def run(self):
        pass

    def stop(self):
        self.stopped.set()
