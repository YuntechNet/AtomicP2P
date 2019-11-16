from multiprocessing import Process, Event

from ..logging import getLogger


class ProcManager(Process):
    def __init__(
        self, loopDelay: int = 1, logger: "logging.Logger" = getLogger(__name__)
    ):
        super().__init__()
        self.logger = logger
        self.loopDelay = loopDelay
        self.stopped = Event()
        self.started = Event()

    def start(self) -> None:
        super().start()
        self.started.set()

    def run(self) -> None:
        pass

    def stop(self) -> None:
        self.stopped.set()
        self.started.clear()

    def is_start(self) -> bool:
        return self.started.is_set()
