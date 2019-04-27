from multiprocessing import Process, Event as pEvent
from threading import Thread, Event as tEvent


class ProcManager(Process):

    def __init__(self, loopDelay: int = 1, output_field=None,
                 auto_register: bool = False) -> None:
        super(ProcManager, self).__init__()
        self.__auto_register = auto_register
        self.output_field = output_field
        self.loopDelay = loopDelay
        self.stopped = pEvent()

    def _register_handler(self) -> None:
        raise NotImplementedError

    def _register_command(self) -> None:
        raise NotImplementedError

    def start(self) -> None:
        super(ProcManager, self).start()
        if self.__auto_register:
            self._register_handler()
            self._register_command()

    def run(self) -> None:
        pass

    def stop(self) -> None:
        self.stopped.set()


class ThreadManager(Thread):

    def __init__(self, loopDelay: int = 1, output_field=None,
                 auto_register: bool = False) -> None:
        super(ThreadManager, self).__init__()
        self.__auto_register = auto_register
        self.output_field = output_field
        self.loopDelay = loopDelay
        self.stopped = tEvent()

    def _register_handler(self) -> None:
        raise NotImplementedError

    def _register_command(self) -> None:
        raise NotImplementedError

    def start(self) -> None:
        super(ThreadManager, self).start()
        if self.__auto_register:
            self._register_handler()
            self._register_command()

    def run(self) -> None:
        pass

    def stop(self) -> None:
        self.stopped.set()
