import traceback
from LibreCisco.utils.manager import ThreadManager
from LibreCisco.utils import printText
from LibreCisco.peer.watchdog.command import (
    HelpCmd, PauseCmd, PeriodCmd, ListCmd, ResetCmd
)
from LibreCisco.peer.watchdog.communication import CheckHandler
from LibreCisco.peer.watchdog.peer_status import PeerStatus


class Watchdog(ThreadManager):

    def __init__(self, peer, loopDelay=2, max_no_response_count=5):
        self.peer = peer
        super(Watchdog, self).__init__(loopDelay=loopDelay,
                                       output_field=peer.output_field,
                                       auto_register=True)

        self.pause = False
        self.max_no_response_count = max_no_response_count
        self.watchdoglist = []

    def run(self):
        while not self.stopped.wait(self.loopDelay):
            if not self.pause:
                no_response_list = []
                for each in self.watchdoglist:
                    addr = each.peer_info.host[0]
                    port = each.peer_info.host[1]
                    data = {'status': each}
                    self.peer.sendMessage((addr, port), 'watchdog_check',
                                          **data)
                    if each.no_response_count >= self.max_no_response_count:
                        no_response_list.append(each)
                self.removeWatchdoglist(no_response_list)

    def registerHandler(self):
        self.handler = {
            'watchdog_check': CheckHandler(self.peer)
        }

    def registerCommand(self):
        self.commands = {
            'help': HelpCmd(self),
            'pause': PauseCmd(self),
            'period': PeriodCmd(self),
            'list': ListCmd(self),
            'reset': ResetCmd(self)
        }

    def onProcess(self, msg_arr):
        msg_key = msg_arr[0].lower()
        msg_arr = msg_arr[1:]
        if msg_key in self.commands:
            return self.commands[msg_key].onProcess(msg_arr)
        return ''

    def onRecvPkt(self, pkt, addr):
        for each in self.peer.connectlist:
            if each.host[0] == addr[0]:
                self.addWatchdoglist(PeerStatus(each))

    def getStatusByHost(self, host):
        peer_info = self.peer.getConnectByHost(host=host)
        if peer_info:
            for each in self.watchdoglist:
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
                return self.addWatchdoglist(PeerStatus(peer_info))
        return None

    def addWatchdoglist(self, peer_status):
        if peer_status not in self.watchdoglist:
            self.watchdoglist.append(peer_status)
            return True
        return False

    def removeStatusByHost(self, host):
        missing = []
        for each in self.watchdoglist:
            if each.peer_info.host[0] == host[0]:
                missing .append(each)
        self.removeWatchdoglist(missing)

    def removeWatchdoglist(self, missing):
        for each in missing:
            try:
                self.watchdoglist.remove(each)
            except Exception as e:
                traceback.print_exc()
