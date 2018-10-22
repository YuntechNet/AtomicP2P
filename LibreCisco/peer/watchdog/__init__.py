import traceback
from LibreCisco.utils.manager import ThreadManager
from LibreCisco.utils import printText
from LibreCisco.peer.watchdog.check import CheckHandler
from LibreCisco.peer.watchdog.peer_status import Peerstatus

class Watchdog(ThreadManager):

    def __init__(self, peer, loopDelay=2):
        self.peer = peer
        super(Watchdog, self).__init__(loopDelay=loopDelay,
                                       output_field=peer.output_field,
                                       auto_register=True)
        self.watchdoglist = []                               
        
    def run(self):
        while not self.stopped.wait(self.loopDelay):
            for each in self.watchdoglist:
                addr = each.peer_info.host[0]
                port = each.peer_info.host[1]
                mes = {'msg': each.nowTime()}
                self.peer.sendMessage((addr, port), 'watchdog_check',
                                      **mes)

    def registerHandler(self):
        self.handler = {
            'watchdog_check': CheckHandler(self.peer)
        }

    def registerCommand(self):
        self.commands = {}

    def onRecvPkt(self, pkt, addr):
        for each in self.peer.connectlist:
            if each.host[0] == addr[0]:
                self.addWatchdoglist(Peerstatus(each))

    def addStatusByHost(self, host):
        peer_info = self.peer.getConnectByHost(host=host)
        if peer_info:
            for each in self.watchdoglist:
                if each.peer_info == peer_info:
                    return False
            return self.addWatchdoglist(Peerstatus(peer_info))
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
        try:
            for each in missing:
                self.watchdoglist.remove(each)            
        except ValueError:
            traceback.print_exc()
