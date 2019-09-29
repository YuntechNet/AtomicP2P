from threading import Thread, Event

from atomic_p2p.logging import getLogger


class ThreadManager(Thread):
    def __init__(
        self, loopDelay: int = 1, logger: "logging.Logger" = getLogger(__name__)
    ):
        super(ThreadManager, self).__init__()
        self.logger = logger
        self.loopDelay = loopDelay
        self.stopped = Event()
        self.started = Event()

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
