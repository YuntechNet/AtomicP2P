import ssl
import socket
import threading

from LibreCisco.peer.peer_info import PeerInfo
from LibreCisco.peer.connection import PeerConnection
from LibreCisco.peer.command import (
    HelpCmd, JoinCmd, SendCmd, ListCmd, LeaveNetCmd
)
from LibreCisco.peer.communication import (
    JoinHandler, CheckJoinHandler, NewMemberHandler, MessageHandler
)
from LibreCisco.peer.monitor.peer_status import PeerStatus, StatusType
from LibreCisco.peer.monitor import Monitor
from LibreCisco.utils import printText
from LibreCisco.utils.manager import ThreadManager
from LibreCisco.utils.command import Command
from LibreCisco.utils.communication import Message


class Peer(ThreadManager):

    def __init__(self, host, name, role, cert, _hash, loopDelay=1,
                 output_field=None):
        super(Peer, self).__init__(loopDelay=loopDelay,
                                   output_field=output_field,
                                   auto_register=True)
        self.peer_info = PeerInfo(name=name, role=role, host=host)
        self._hash = _hash
        printText('Program hash: {{{}...{}}}'.format(_hash[:6], _hash[-6:]))
        self.cert = cert
        self.setServer(cert)
        self.connectlist = []
        self.monitor = Monitor(self)
        self.last_output = ''

    def registerHandler(self):
        self.handler = {
            'join': JoinHandler(self),
            'checkjoin': CheckJoinHandler(self),
            'newmember': NewMemberHandler(self),
            'message': MessageHandler(self)
        }

    def registerCommand(self):
        self.commands = {
            'help': HelpCmd(self),
            'join': JoinCmd(self),
            'send': SendCmd(self),
            'list': ListCmd(self),
            'leavenet': LeaveNetCmd(self)
        }

    def onProcess(self, msg_arr, **kwargs):
        msg_key = msg_arr[0].lower()
        msg_arr = msg_arr[1:]
        if msg_key in self.commands:
            return self.commands[msg_key]._on_process(msg_arr)
        return self.commands['help']._on_process(msg_arr)

    def start(self):
        super(Peer, self).start()
        self.monitor.start()

    def run(self):
        while not self.stopped.wait(self.loopDelay):
            (conn, addr) = self.server.accept()
            accepthandle = threading.Thread(target=self.acceptHandle,
                                            args=(conn, addr))
            accepthandle.start()

    def stop(self):
        self.monitor.stop()
        self.stopped.set()
        self.sendMessage(('127.0.0.1', self.peer_info.host[1]), 'message',
                         **{'msg': 'disconnect successful.'})
        self.server.close()

    # accept
    def setServer(self, cert):
        unwrap_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        unwrap_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        unwrap_socket.bind(self.peer_info.host)
        unwrap_socket.listen(5)
        self.server = ssl.wrap_socket(unwrap_socket, certfile=cert[0],
                                      keyfile=cert[1], server_side=True)
        printText('Peer prepared')
        printText('This peer is running with certificate at path {}'.format(
                    cert[0]))
        printText('Please make sure other peers have same certicate.')

    def selectHandler(self, _type):
        if _type in self.handler:
            return self.handler[_type]
        elif _type in self.monitor.handler:
            return self.monitor.handler[_type]
        else:
            return None

    def acceptHandle(self, conn, addr):
        pkt = Message.recv(conn.recv(1024))
        in_net = self.containsInConnectlist(addr[0])
        hash_match = self._hash == pkt._hash
        handler = self.selectHandler(pkt._type)

        if handler:
            if hash_match is False and pkt.is_reject() is False:
                printText(('Illegal peer {} with unmatch hash {{{}...{}}} '
                           'trying to connect to net.').format(
                            addr, pkt._hash[:6], pkt._hash[-6:]))
                self.sendMessage(pkt._from, pkt._type,
                                 **{'reject_reason': 'Unmatching peer hash.'})
            elif in_net is True or pkt._type in ['join', 'checkjoin']:
                handler.onRecv(src=addr, pkt=pkt)
                self.monitor.onRecvPkt(addr=pkt._from, pkt=pkt)
            else:
                self.sendMessage(pkt._from, pkt._type,
                                 **{'reject_reason': 'not in current net'})
        else:
            printText('Unknown packet tpye: {}'.format(pkt._type))

    # send
    def sendMessage(self, host, sendType, **kwargs):
        handler = self.selectHandler(sendType)
        if handler:
            messages = handler.onSend(target=host, **kwargs)
            for each in messages:
                sender = PeerConnection(peer=self, message=each,
                                        cert_pem=self.cert[0],
                                        output_field=self.output_field)
                sender.start()
        else:
            printText('No such type.')

    # list
    def containsInConnectlist(self, host):
        for each in self.connectlist:
            if each.host[0] == host:
                return True
        return False

    def getConnectByHost(self, host):
        for each in self.connectlist:
            if each.host == host:
                return each
        return None

    def getConnectByName(self, name):
        for each in self.connectlist:
            if each.name == name:
                return each
        return None

    def addConnectlist(self, peer_info):
        if peer_info not in self.connectlist:
            self.connectlist.append(peer_info)
            self.monitor.addMonitorlist(PeerStatus(peer_info))

    def removeConnectlist(self, peer_info):
        try:
            self.connectlist.remove(peer_info)
            return True
        except ValueError:
            return False
