from multiprocessing import Process, Event as pEvent
from threading import Thread, Event as tEvent

from atomic_p2p.utils.logging import getLogger


class ProcManager(Process):
    def __init__(
        self,
        loopDelay: int = 1,
        logger: "logging.Logger" = getLogger(__name__),
    ):
        super(ProcManager, self).__init__()
        self.logger = logger
        self.loopDelay = loopDelay
        self.stopped = pEvent()
        self.started = pEvent()

    def start(self) -> None:
        super(ProcManager, self).start()
        self.started.set()

    def run(self) -> None:
        pass

    def stop(self) -> None:
        self.stopped.set()
        self.started.clear()

    def is_start(self) -> bool:
        return self.started.is_set()


class ThreadManager(Thread):
    def __init__(
        self,
        loopDelay: int = 1,
        logger: "logging.Logger" = getLogger(__name__),
    ):
        super(ThreadManager, self).__init__()
        self.logger = logger
        self.loopDelay = loopDelay
        self.stopped = tEvent()
        self.started = tEvent()

    def start(self) -> None:
        super(ThreadManager, self).start()
        self.started.set()

    def run(self) -> None:
        pass

    def stop(self) -> None:
        self.stopped.set()
        self.started.clear()

    def is_start(self) -> bool:
        return self.started.is_set()
