import traceback
from typing import Tuple, List

from atomic_p2p.utils.manager import ThreadManager
from atomic_p2p.peer.monitor.command import (
    HelpCmd, PauseCmd, PeriodCmd, ListCmd, ResetCmd, VerboseCmd, ManualCmd
)
from atomic_p2p.peer.monitor.communication import CheckHandler
from atomic_p2p.utils.logging import getLogger


class Monitor(ThreadManager):

    def __init__(self, peer: 'Peer', loopDelay: int = 10,
                 verbose: bool = False, max_no_response_count: int = 5):
        self.peer = peer
        super(Monitor, self).__init__(loopDelay=loopDelay, auto_register=True,
                                      logger=getLogger(__name__))
        self.verbose = False
        self.pause = False
        self.max_no_response_count = max_no_response_count

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

    def onProcess(self, msg_arr):
        try:
            msg_key = msg_arr[0].lower()
            msg_arr = msg_arr[1:]
            if msg_key in self.commands:
                return self.commands[msg_key]._on_process(msg_arr)
            return self.commands['help']._on_process(msg_arr)
        except Exception:
            return self.commands['help']._on_process(msg_arr)

    def on_recv_pkt(self, addr: Tuple[str, int],
                    pkt: 'Packet', conn: 'SSLSocket') -> None:
        if not pkt.is_reject():
            peer_info = self.peer.get_peer_info_by_host(host=pkt.src)
            if peer_info is not None:
                peer_info.status.update()

    def removeMonitorlist(self, missing: List) -> None:
        for each in missing:
            try:
                self.peer.pend_socket_to_rm(each.conn)
                self.logger.info(('{} has been remove from '
                                  'status list.').format(each))
            except Exception:
                self.logger.error(traceback.format_exc())

    def _register_handler(self) -> None:
        installing_handlers = [
            CheckHandler(self)
        ]
        for each in installing_handlers:
            self.register_handler(handler=each)

    def _register_command(self) -> None:
        installing_commands = [
            HelpCmd(self), PauseCmd(self), PeriodCmd(self), ListCmd(self),
            ResetCmd(self), VerboseCmd(self), ManualCmd(self)
        ]
        for each in installing_commands:
            self.register_command(command=each)
