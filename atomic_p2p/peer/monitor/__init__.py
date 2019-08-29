import traceback
from typing import Tuple, List
from threading import Thread, Event as tEvent

from atomic_p2p.utils.manager import ThreadManager
from atomic_p2p.peer.monitor.command import (
    HelpCmd, PauseCmd, PeriodCmd, ListCmd, ResetCmd, VerboseCmd, ManualCmd
)
from atomic_p2p.peer.monitor.communication import CheckHandler
from atomic_p2p.utils.logging import getLogger


class Monitor(Thread):

    def __init__(self, peer: "Peer", loop_delay: int = 10,
                 verbose: bool = False, max_no_response_count: int = 5,
                 logger: "logging.Logger" = getLogger(__name__)):
        self.peer = peer
        super(Monitor, self).__init__()
        self.logger = logger
        self.loopDelay = loop_delay
        self.stopped = tEvent()
        self.started = tEvent()

        self.verbose = False
        self.pause = False
        self.max_no_response_count = max_no_response_count

        self.pkt_handlers = {}
        self.commands = {}

    def start(self) -> None:
        super().start()
        self._register_handler()
        self._register_command()
        self.started.set()

    def stop(self) -> None:
        self.stopped.set()
        self.started.clear()

    def is_start(self) -> bool:
        return self.started.is_set()

    def run(self) -> None:
        while not self.stopped.wait(self.loopDelay):
            if self.pause is False:
                no_response_list = []
                for (host, peer_info) in self.peer.peer_pool.items():
                    self.peer.handler_unicast_packet(
                        host=host, pkt_type=CheckHandler.pkt_type)
                    if peer_info.status.no_response_count >= \
                            self.max_no_response_count:
                        no_response_list.append(peer_info)
                self.removeMonitorlist(no_response_list)

    def select_handler(self, pkt_type: str) -> "Handler":
        if pkt_type in self.pkt_handlers:
            return self.pkt_handlers[pkt_type]
        return None

    def onProcess(self, msg_arr, **kwargs) -> str:
        self.logger.warning("[Deprecated] onProcess method is no longer maintai"
            "n, manually send command into peer is not recommended.")
        return self._on_command(msg_arr, **kwargs)

    def _on_command(self, msg_arr: list, **kwargs) -> str:
        try:
            msg_key = msg_arr[0].lower()
            msg_arr = msg_arr[1:]
            if msg_key in self.commands:
                return self.commands[msg_key]._on_command_recv(msg_arr)
            return self.commands["help"]._on_command_recv(msg_arr)
        except Exception:
            return self.commands["help"]._on_command_recv(msg_arr)

    def on_recv_pkt(self, addr: Tuple[str, int],
                    pkt: "Packet", conn: "SSLSocket") -> None:
        if not pkt.is_reject():
            peer_info = self.peer.get_peer_info_by_host(host=pkt.src)
            if peer_info is not None:
                peer_info.status.update()

    def removeMonitorlist(self, missing: List) -> None:
        for each in missing:
            try:
                self.peer.pend_socket_to_rm(each.conn)
                self.logger.info(("{} has been remove from "
                                  "status list.").format(each))
            except Exception:
                self.logger.error(traceback.format_exc())

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

    def _register_handler(self) -> None:
        installing_handlers = [
            CheckHandler(self)
        ]
        for each in installing_handlers:
            self.register_handler(handler=each)

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

    def _register_command(self) -> None:
        installing_commands = [
            HelpCmd(self), PauseCmd(self), PeriodCmd(self), ListCmd(self),
            ResetCmd(self), VerboseCmd(self), ManualCmd(self)
        ]
        for each in installing_commands:
            self.register_command(command=each)
