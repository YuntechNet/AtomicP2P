from multiprocessing import Process, Event as pEvent
from threading import Thread, Event as tEvent
from atomic_p2p.utils.logging import getLogger


class ProcManager(Process):

    def __init__(self, loopDelay: int = 1, auto_register: bool = False,
                 logger=None):
        super(ProcManager, self).__init__()
        self.__auto_register = auto_register
        self.logger = getLogger(__name__) if logger is None else logger
        self.loopDelay = loopDelay
        self.stopped = pEvent()
        self.started = pEvent()

    def _register_handler(self) -> None:
        raise NotImplementedError

    def _register_command(self) -> None:
        raise NotImplementedError

    def start(self) -> None:
        super(ProcManager, self).start()
        if self.__auto_register:
            self._register_handler()
            self._register_command()
        self.started.set()

    def run(self) -> None:
        pass

    def stop(self) -> None:
        self.stopped.set()
        self.started.clear()

    def is_start(self):
        return self.started.is_set()


class ThreadManager(Thread):

    def __init__(self, loopDelay: int = 1, auto_register: bool = False,
                 logger=None):
        super(ThreadManager, self).__init__()
        self.__auto_register = auto_register
        self.logger = getLogger(__name__) if logger is None else logger
        self.loopDelay = loopDelay
        self.stopped = tEvent()
        self.started = tEvent()

    def _register_handler(self) -> None:
        raise NotImplementedError

    def _register_command(self) -> None:
        raise NotImplementedError

    def start(self) -> None:
        super(ThreadManager, self).start()
        if self.__auto_register:
            self._register_handler()
            self._register_command()
        self.started.set()

    def run(self) -> None:
        pass

    def stop(self) -> None:
        self.stopped.set()
        self.started.clear()

    def is_start(self):
        return self.started.is_set()
