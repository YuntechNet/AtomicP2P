from multiprocessing import Process, Event as pEvent
from threading import Thread, Event as tEvent
from atomic_p2p.utils.logging import getLogger


class ProcManager(Process):

    def __init__(self, loopDelay: int = 1, auto_register: bool = False,
                 logger: "logging.Logger" = getLogger(__name__)):
        super(ProcManager, self).__init__()
        self.__auto_register = auto_register
        self.logger = logger
        self.loopDelay = loopDelay
        self.stopped = pEvent()
        self.started = pEvent()

        self.pkt_handlers = {}
        self.commands = {}

    def select_handler(self, pkt_type: str) -> "Handler":
        if pkt_type in self.pkt_handlers:
            return self.pkt_handlers[pkt_type]
        return None

    def register_handler(self, handler: "Handler",
                         force: bool = False) -> bool:
        """Register the handler with it's pkt_type to pkt_handlers

        Args:
            handler: The handler to be register.
            force: If handler is exists, weather override it or not.

        Returns:
            True if handler been set, False is fail.
        """
        if handler.pkt_type not in self.pkt_handlers or force is True:
            self.pkt_handlers[type(handler).pkt_type] = handler
            return True
        return False

    def unregister_handler(self, pkt_type: str) -> bool:
        """Unregister a handler in pkt_handlers

        Args:
            pkt_type: Target handler's pkt_type to unregister.

        Returns:
            True if remove success, False means not exists.
        """
        if pkt_type in self.pkt_handlers:
            del self.pkt_handlers[pkt_type]
            return True
        return False

    def _register_handler(self) -> None:
        raise NotImplementedError

    def register_command(self, command: "Command",
                         force: bool = False) -> bool:
        """Register the command with it's cmd to commands

        Args:
            command: The command to be register.
            force: If command is exists, weather override it or not.

        Returns:
            True if command been set, False is fail.
        """
        if command.cmd not in self.commands or force is True:
            self.commands[command.cmd] = command
            return True
        return False

    def unregister_command(self, cmd: str) -> bool:
        """Unregister a command in commands

        Args:
            cmd: Target command's key cmd to unregister.

        Returns:
            True if remove success, False means not exists.
        """
        if cmd in self.commands:
            del self.commands[cmd]
            return True
        return False

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

    def is_start(self) -> bool:
        return self.started.is_set()


class ThreadManager(Thread):

    def __init__(self, loopDelay: int = 1, auto_register: bool = False,
                 logger: "logging.Logger" = getLogger(__name__)):
        super(ThreadManager, self).__init__()
        self.__auto_register = auto_register
        self.logger = logger
        self.loopDelay = loopDelay
        self.stopped = tEvent()
        self.started = tEvent()

        self.pkt_handlers = {}
        self.commands = {}

    def select_handler(self, pkt_type: str) -> "Handler":
        if pkt_type in self.pkt_handlers:
            return self.pkt_handlers[pkt_type]
        return None

    def register_handler(self, handler: "Handler",
                         force: bool = False) -> bool:
        """Register the handler with it's pkt_type to pkt_handlers

        Args:
            handler: The handler to be register.
            force: If handler is exists, weather override it or not.

        Returns:
            True if handler been set, False is fail.
        """
        if handler.pkt_type not in self.pkt_handlers or force is True:
            self.pkt_handlers[type(handler).pkt_type] = handler
            return True
        return False

    def unregister_handler(self, pkt_type: str) -> bool:
        """Unregister a handler in pkt_handlers

        Args:
            pkt_type: Target handler's pkt_type to unregister.

        Returns:
            True if remove success, False means not exists.
        """
        if pkt_type in self.pkt_handlers:
            del self.pkt_handlers[pkt_type]
            return True
        return False

    def _register_handler(self) -> None:
        raise NotImplementedError

    def register_command(self, command: "Command",
                         force: bool = False) -> bool:
        """Register the command with it's cmd to commands

        Args:
            command: The command to be register.
            force: If command is exists, weather override it or not.

        Returns:
            True if command been set, False is fail.
        """
        if command.cmd not in self.commands or force is True:
            self.commands[command.cmd] = command
            return True
        return False

    def unregister_command(self, cmd: str) -> bool:
        """Unregister a command in commands

        Args:
            cmd: Target command's key cmd to unregister.

        Returns:
            True if remove success, False means not exists.
        """
        if cmd in self.commands:
            del self.commands[cmd]
            return True
        return False

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

    def is_start(self) -> bool:
        return self.started.is_set()
