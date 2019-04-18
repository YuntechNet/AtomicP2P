from time import sleep

from LibreCisco.utils import printText
from LibreCisco.utils.command import Command
from LibreCisco.peer.entity.peer_info import PeerInfo
from LibreCisco.peer.communication.net import JoinHandler, DisconnectHandler
from LibreCisco.peer.communication.msg import MessageHandler


class HelpCmd(Command):
    """HelpCmd
        show the help for peers.
        Usage in prompt: peer help [cmd]
    """

    def __init__(self, peer):
        super(HelpCmd, self).__init__('help')
        self.peer = peer
        self.output_field = peer.output_field

    def onProcess(self, msg_arr):
        if msg_arr != [] and msg_arr[0] in self.peer.commands:
            printText(self.peer.commands[msg_arr[0]].__doc__)
        else:
            printText("peer [cmd] <options>\n"
                      " - join [ip:port]                                 "
                      "send a join net request to a exists net peer.\n"
                      " - send [ip:port/broadcast:role] [msg]            "
                      "send a msg to host.\n"
                      " - list                                           "
                      "list all peer's info in know peer list.\n"
                      " - leavenet                                       "
                      "leave current net.\n"
                      " - help [cmd]                                     "
                      "show help msg of sepecific command.")


class JoinCmd(Command):
    """JoinCmd
        send a join request to a peer.
        Usage in prompt: peer join [ip:port]
    """

    def __init__(self, peer):
        super(JoinCmd, self).__init__('join')
        self.peer = peer

    def onProcess(self, msg_arr):
        addr = msg_arr[0].split(':')
        addr[1] = int(addr[1])
        handler = self.peer.select_handler(pkt_type=JoinHandler.pkt_type)
        pkt = handler.on_send(target=(addr[0], addr[1]))

        sock = self.peer.new_tcp_long_conn(dst=(addr[0], addr[1]))
        self.peer.pend_socket(sock=sock)
        self.peer.pend_packet(sock=sock, pkt=pkt)


class SendCmd(Command):
    """SendCmd
        send a message to a specific peer or broadcast in prompt.
        Usage in prompt: peer send [ip:port/broadcast:all] [msg]
    """

    def __init__(self, peer):
        super(SendCmd, self).__init__('send')
        self.peer = peer

    def onProcess(self, msg_arr):
        msg_key = msg_arr[0]
        msg_arr = msg_arr[1:]
        addr = msg_key.split(':')
        mes = {'msg': msg_arr}
        try:
            addr[1] = int(addr[1])
            self.peer.handler_unicast_packet(
                host=(addr[0], addr[1]), pkt_type=MessageHandler.pkt_type,
                **mes)
        except ValueError:
            self.peer.handler_broadcast_packet(
                host=(addr[0], addr[1]), pkt_type=MessageHandler.pkt_type,
                **mes)


class ListCmd(Command):
    """ListCmd
        list every linked peer's host message in prompt.
        Usage in prompt: peer list
    """

    def __init__(self, peer):
        super(ListCmd, self).__init__('list')
        self.peer = peer
        self.output_field = peer.output_field

    def onProcess(self, msg_arr):
        if len(self.peer.connectlist) == 0:
            printText('There is no peers in current net.')
        else:
            printText('There is the connection list of peers in current net:')
            for each in self.peer.connectlist:
                printText(' - ' + str(each))
            printText('[---End of list---]')


class LeaveNetCmd(Command):
    """LeaveNetCmd
        leave the current net, this will clear monitor list and peer list.
        Usage in prompt: peer leavenet
    """

    def __init__(self, peer):
        super(LeaveNetCmd, self).__init__('leavenet')
        self.peer = peer
        self.output_field = peer.output_field

    def onProcess(self, msg_arr):
        handler = self.peer.select_handler(pkt_type=DisconnectHandler.pkt_type)
        for each in list(self.peer.connectlist):
            # TODO: Fit unittest empty conn in PeerInfo
            #       Waiting for use mock.
            #               - 2019/04/13
            if each.conn is None:
                continue
            pkt = handler.on_send(target=each.host)
            self.peer.pend_packet(sock=each.conn, pkt=pkt)
        self.peer.peer_pool = {}
        printText('You left net.')
