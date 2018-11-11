from multiprocessing import Process, Event as pEvent
from threading import Thread, Event as tEvent
from LibreCisco.utils.logging import getLogger


class ProcManager(Process):

    def __init__(self, loopDelay=1, auto_register=False,
                 logger=None):
        super(ProcManager, self).__init__()
        self.logger = getLogger(__name__) if logger is None else logger
        self.loopDelay = loopDelay
        self.stopped = pEvent()
        self.started = pEvent()

        if auto_register:
            self.registerHandler()
            self.registerCommand()

    def registerHandler(self):
        raise NotImplementedError

    def registerCommand(self):
        raise NotImplementedError

    def start(self):
        super(ProcManager, self).start()
        self.started.set()

    def run(self):
        pass

    def stop(self):
        self.stopped.set()
        self.started.clear()

    def is_start(self):
        return self.started.is_set()


class ThreadManager(Thread):

    def __init__(self, loopDelay=1, auto_register=False,
                 logger=None):
        super(ThreadManager, self).__init__()
        self.logger = getLogger(__name__) if logger is None else logger
        self.loopDelay = loopDelay
        self.stopped = tEvent()
        self.started = tEvent()

        if auto_register:
            self.registerHandler()
            self.registerCommand()

    def registerHandler(self):
        raise NotImplementedError

    def registerCommand(self):
        raise NotImplementedError

    def start(self):
        super(ThreadManager, self).start()
        self.started.set()

    def run(self):
        pass

    def stop(self):
        self.stopped.set()
        self.started.clear()

    def is_start(self):
        return self.started.is_set()
