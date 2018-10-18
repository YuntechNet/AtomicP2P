from multiprocessing import Process, Event as pEvent
from threading import Thread, Event as tEvent


class ProcManager(Process):

    def __init__(self, loopDelay=1, output_field=None, auto_register=False):
        super(ProcManager, self).__init__()
        self.output_field = output_field
        self.loopDelay = loopDelay
        self.stopped = pEvent()

        if auto_register:
            self.registerHandler()
            self.registerCommand()

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

    def __init__(self, loopDelay=1, output_field=None, auto_register=False):
        super(ThreadManager, self).__init__()
        self.output_field = output_field
        self.loopDelay = loopDelay
        self.stopped = tEvent()

        if auto_register:
            self.registerHandler()
            self.registerCommand()

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
