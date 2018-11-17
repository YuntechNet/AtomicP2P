import traceback
from LibreCisco.utils.manager import ThreadManager
from LibreCisco.peer.monitor.command import (
    HelpCmd, PauseCmd, PeriodCmd, ListCmd, ResetCmd, VerboseCmd, ManualCmd
)
from LibreCisco.peer.monitor.communication import CheckHandler
from LibreCisco.peer.monitor.peer_status import PeerStatus
from LibreCisco.utils.logging import getLogger


class Monitor(ThreadManager):

    def __init__(self, peer, loopDelay=2, verbose=False,
                 max_no_response_count=5):
        self.peer = peer
        super(Monitor, self).__init__(loopDelay=loopDelay, auto_register=True,
                                      logger=getLogger(__name__))
        self.verbose = False
        self.pause = False
        self.max_no_response_count = max_no_response_count
        self.monitorlist = []

    def run(self):
        while not self.stopped.wait(self.loopDelay):
            if not self.pause:
                no_response_list = []
                for each in self.monitorlist:
                    addr = each.peer_info.host[0]
                    port = each.peer_info.host[1]
                    self.peer.sendMessage((addr, port), 'monitor_check')
                    if each.no_response_count >= self.max_no_response_count:
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
        try:
            msg_key = msg_arr[0].lower()
            msg_arr = msg_arr[1:]
            if msg_key in self.commands:
                return self.commands[msg_key].onProcess(msg_arr)
            return self.commands['help']._on_process(msg_arr)
        except Exception as e:
            return self.commands['help']._on_process(msg_arr)

    def onRecvPkt(self, addr, pkt):
        if not pkt.is_reject():
            status, peer_info = self.getStatusByHost(host=pkt._from)
            if status is not None:
                status.update()
            elif peer_info is not None:
                self.addMonitorlist(PeerStatus(peer_info=peer_info))
            else:
                pass

    def getStatusByHost(self, host):
        peer_info = self.peer.getConnectByHost(host=host)
        if peer_info:
            for each in self.monitorlist:
                if each.peer_info == peer_info:
                    return each, peer_info
        return None, peer_info

    def updateStatusByHost(self, host):
        status, peer_info = self.getStatusByHost(host=host)
        if peer_info:
            if status:
                status.update()
                return False
            else:
                return self.addMonitorlist(PeerStatus(peer_info))
        return None

    def addMonitorlist(self, peer_status):
        if peer_status not in self.monitorlist:
            self.monitorlist.append(peer_status)
            return True
        return False

    def removeStatusByHost(self, host):
        missing = []
        for each in self.monitorlist:
            if each.peer_info.host == host:
                missing .append(each)
        self.removeMonitorlist(missing)

    def removeMonitorlist(self, missing):
        for each in missing:
            try:
                self.monitorlist.remove(each)
                self.logger.info(('{} has been remove from '
                                  'status list.').format(each))
            except Exception as e:
                self.logger.error(traceback.format_exc())
