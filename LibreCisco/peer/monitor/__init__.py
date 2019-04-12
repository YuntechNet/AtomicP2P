import traceback
from LibreCisco.utils.manager import ThreadManager
from LibreCisco.utils import printText
from LibreCisco.peer.monitor.command import (
    HelpCmd, PauseCmd, PeriodCmd, ListCmd, ResetCmd, VerboseCmd, ManualCmd
)
from LibreCisco.peer.monitor.communication import CheckHandler
from LibreCisco.peer.entity.peer_status import PeerStatus


class Monitor(ThreadManager):

    def __init__(self, peer, loopDelay=2, verbose=False,
                 max_no_response_count=5):
        self.peer = peer
        super(Monitor, self).__init__(loopDelay=loopDelay,
                                      output_field=peer.output_field,
                                      auto_register=True)

        self.verbose = False
        self.pause = False
        self.max_no_response_count = max_no_response_count
        self.monitorlist = []

    def run(self):
        while not self.stopped.wait(self.loopDelay):
            if not self.pause:
                no_response_list = []
                for each in self.peer.connectlist:
                    self.peer.sendMessage(each.host, 'monitor_check')
                    if each.status.no_response_count >= \
                            self.max_no_response_count:
                        no_response_list.append(each)
                self.removeMonitorlist(no_response_list)

    def registerHandler(self):
        self.handler = {
            'monitor_check': CheckHandler(self)
        }

    def registerCommand(self):
        self.commands = {
            'help': HelpCmd(self),
            'pause': PauseCmd(self),
            'period': PeriodCmd(self),
            'list': ListCmd(self),
            'reset': ResetCmd(self),
            'verbose': VerboseCmd(self),
            'manual': ManualCmd(self)
        }

    def onProcess(self, msg_arr):
        msg_key = msg_arr[0].lower()
        msg_arr = msg_arr[1:]
        if msg_key in self.commands:
            return self.commands[msg_key].onProcess(msg_arr)
        return ''

    def onRecvPkt(self, addr, pkt):
        if not pkt.is_reject():
            status, peer_info = self.getStatusByHost(host=pkt._from)
            if peer_info is not None:
                status.update()
            else:
                pass

    def getStatusByHost(self, host):
        peer_info = self.peer.getConnectByHost(host=host)
        return (peer_info.status if peer_info else None, peer_info)

    def removeMonitorlist(self, missing):
        for each in missing:
            try:
                self.peer.removeConnectlist(each)
                printText('{} has been remove from peer list.'.format(each))
            except Exception as e:
                printText(traceback.format_exc())
