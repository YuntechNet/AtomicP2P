import ssl
import socket
import select
import threading
from time import sleep

from LibreCisco.peer.entity.peer_info import PeerInfo
from LibreCisco.peer.connection import PeerTCPLongConn
from LibreCisco.peer.command import (
    HelpCmd, JoinCmd, SendCmd, ListCmd, LeaveNetCmd
)
from LibreCisco.peer.communication import (
    JoinHandler, CheckJoinHandler, NewMemberHandler, AckNewMemberHandler,
    DisconnectHandler, MessageHandler
)
from LibreCisco.peer.monitor import Monitor
from LibreCisco.utils import printText, host_valid
from LibreCisco.utils.manager import ThreadManager
from LibreCisco.utils.command import Command
from LibreCisco.utils.communication import Packet


class Peer(ThreadManager):

    def __init__(self, host, name, role, cert, _hash, loopDelay=1,
                 output_field=None):
        super(Peer, self).__init__(loopDelay=loopDelay,
                                   output_field=output_field,
                                   auto_register=True)
        self.pending_conns = []
        self.terminating_fds = []
        self.in_fds = []
        self.out_fds = []
        self.ex_fds = []

        self.peer_info = PeerInfo(name=name, role=role, host=host)
        self._hash = _hash
        printText('Program hash: {{{}...{}}}'.format(_hash[:6], _hash[-6:]))
        self.cert = cert
        self.setServer(cert)
        self.connectlist = []
        self.monitor = Monitor(self)
        self.last_output = ''

    def registerHandler(self):
        installed_handler = [
            JoinHandler(self), CheckJoinHandler(self), NewMemberHandler(self),
            MessageHandler(self), AckNewMemberHandler(self),
            DisconnectHandler(self)
        ]
        self.handler = {}
        for each in installed_handler:
            self.handler[type(each).pkt_type] = each

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
            return self.commands[msg_key].onProcess(msg_arr)
        return ''

    def start(self):
        super(Peer, self).start()
        self.monitor.start()

    def run(self):
        while not self.stopped.wait(self.loopDelay) or \
              len(self.terminating_fds) > 0:
            readable, writable, exceptional = select.select(
                self.in_fds, self.out_fds, self.ex_fds, self.loopDelay)
            for s in readable:
                if s is self.server:
                    conn, addr = s.accept()
                    tcpLongConn = \
                        PeerTCPLongConn(peer=self, conn=conn, host=addr)
                    tcpLongConn.unblock_recv()
                else:
                    peer_info = self.get_peer_info_by_socket(socket=s)
                    pending_conn = self.get_pending_conn_by_socket(socket=s)
                    if peer_info is not None:
                        peer_info.conn.unblock_recv()
                    elif pending_conn is not None:
                        pending_conn.unblock_recv()

            for s in writable:
                peer_info = self.get_peer_info_by_socket(socket=s)
                pending_conn = self.get_pending_conn_by_socket(socket=s)
                if peer_info is not None:
                    peer_info.conn.unblock_send()
                elif pending_conn is not None:
                    pending_conn.unblock_send()

            for s in exceptional:
                peer_info = self.get_peer_info_by_socket(socket=s)
                if peer_info is not None:
                    pass
                print(s)
        self.server.close()
        print('Stopped')

    def stop(self):
        self.monitor.stop()
        self.stopped.set()
        for each in self.connectlist:
            if each.conn is None:
                continue
            each.conn.sendMessage(host=each.host,
                                  pkt_type=DisconnectHandler.pkt_type)
            each.conn.unblock_send()

    # accept
    def setServer(self, cert):
        unwrap_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        unwrap_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        unwrap_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        unwrap_socket.bind(self.peer_info.host)
        unwrap_socket.listen(5)
        unwrap_socket.setblocking(False)
        self.server = ssl.wrap_socket(unwrap_socket, certfile=cert[0],
                                      keyfile=cert[1], server_side=True)
        self.in_fds.append(self.server)
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

    def handler_unicast_packet(self, host, pkt_type, **kwargs):
        assert host_valid(host) is True
        handler = self.selectHandler(_type=pkt_type)
        if handler is None:
            printText('Unknow handler pkt_type')
        elif self.containsInNet(host=host):
            pkt = handler.on_send(target=host, **kwargs)
            peer_info = self.getConnectByHost(host=host)
            peer_info.conn.send_packet(pkt=pkt)
        else:
            printText('Host not in current net.')

    def handler_broadcast_packet(self, host, pkt_type, **kwargs):
        handler = self.selectHandler(_type=pkt_type)
        if handler is None:
            printText('Unknow handler pkt_type')
        else:
            for each in self.connectlist:
                if host[1] == 'all' or host[1] == each.role:
                    pkt = handler.on_send(target=each.host, **kwargs)
                    each.conn.send_packet(pkt=pkt)

    def new_tcp_long_conn(self, host):
        assert host_valid(host) is True
        return PeerTCPLongConn(peer=self, host=host, conn=None,
                               cert_pem=self.cert[0])

    def get_peer_info_by_socket(self, socket):
        # TODO: This is a transite function before rebuild PeerInfo and
        #       PeerTCPLongConn's inherit structure.
        for each in self.connectlist:
            if each.conn.conn == socket:
                return each
        return None

    def remove_fd_by_socket(self, socket):
        # TODO: This is a transite function before rebuild PeerInfo and
        #       PeerTCPLongConn's inherit structure.
        if socket in self.in_fds:
            self.in_fds.remove(socket)
        if socket in self.out_fds:
            self.out_fds.remove(socket)
        if socket in self.ex_fds:
            self.ex_fds.remove(socket)
        if socket in self.terminating_fds:
            self.terminating_fds.remove(socket)

    def remove_peer_info_by_socket(self, socket):
        # TODO: This is a transite function before rebuild PeerInfo and
        #       PeerTCPLongConn's inherit structure.
        for each in list(self.connectlist):
            if each.conn.conn == socket:
                self.connectlist.remove(each)

    def get_pending_conn_by_socket(self, socket):
        # TODO: This is a transite function before rebuild PeerInfo and
        #       PeerTCPLongConn's inherit structure.
        for each in self.pending_conns:
            if each.conn == socket:
                return each
        return None

    def containsInNet(self, host):
        assert host_valid(host) is True
        for each in self.connectlist:
            if each.host == host:
                return True
        return False

    def getConnectByHost(self, host):
        for each in self.connectlist:
            if each.host == host:
                return each
        return None

    def addConnectlist(self, peer_info):
        if peer_info not in self.connectlist:
            self.connectlist.append(peer_info)
            # TODO: This is a transite function before rebuild PeerInfo and
            #       PeerTCPLongConn's inherit structure.
            if peer_info.conn in self.pending_conns:
                self.pending_conns.remove(peer_info.conn)

    def removeConnectlist(self, peer_info):
        try:
            self.connectlist.remove(peer_info)
            # TODO: This is a transite function before rebuild PeerInfo and
            #       PeerTCPLongConn's inherit structure.
            if peer_info.conn is not None:
                if peer_info.conn.conn not in self.terminating_fds:
                    self.terminating_fds.append(peer_info.conn.conn)
            return True
        except ValueError:
            return False
