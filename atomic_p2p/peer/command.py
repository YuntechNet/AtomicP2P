from atomic_p2p.utils.command import Command
from atomic_p2p.utils.communication import is_ssl_socket_open
from atomic_p2p.peer.entity.peer_info import PeerInfo
from atomic_p2p.peer.communication.net import JoinHandler, DisconnectHandler
from atomic_p2p.peer.communication.msg import MessageHandler


class HelpCmd(Command):
    """HelpCmd
        show the help for peers.
        Usage in prompt: peer help [cmd]
    """

    def __init__(self, peer):
        super(HelpCmd, self).__init__('help')
        self.peer = peer

    def onProcess(self, msg_arr):
        if msg_arr != [] and msg_arr[0] in self.peer.commands:
            return self.peer.commands[msg_arr[0]].__doc__
        else:
            return ("peer [cmd] <options>\n"
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
        Usage in prompt:
            peer join IP:PORT
            peer join DOMAIN [NS1,NS2,NS3]
    """

    def __init__(self, peer):
        super(JoinCmd, self).__init__('join')
        self.peer = peer

    def onProcess(self, msg_arr):
        if ':' in msg_arr[0]:
            addr = msg_arr[0].split(':')
            addr[1] = int(addr[1])
        else:
            peer_info = self._get_online_peer_from_DNS(
                domain=msg_arr[0], ns=msg_arr[1] if len(msg_arr) == 2 else None
            )
            addr = peer_info.host
        handler = self.peer.select_handler(pkt_type=JoinHandler.pkt_type)
        pkt = handler.on_send(target=(addr[0], addr[1]))

        sock = self.peer.new_tcp_long_conn(dst=(addr[0], addr[1]))
        self.peer.pend_socket(sock=sock)
        self.peer.pend_packet(sock=sock, pkt=pkt)

    def _get_online_peer_from_DNS(self, domain, ns=None):
        if ns is not None and type(ns) is not list:
            self.peer.dns_resolver.change_ns(ns=ns.split(','))
        records = self.peer.dns_resolver.sync_from_DNS(
            current_host=self.peer.server_info.host, domain=domain)
        for each in records:
            if is_ssl_socket_open(host=each.host) is True:
                return each
        raise ValueError('No Online peer in dns records.')
        


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

    def onProcess(self, msg_arr):
        if len(self.peer.connectlist) == 0:
            return 'There is no peers in current net.'
        else:
            output_text = 'Current peers info:'
            for each in self.peer.connectlist:
                output_text += (' - ' + str(each) + '\n')
            output_text += '[---End of list---]'
            return output_text


class LeaveNetCmd(Command):
    """LeaveNetCmd
        leave the current net, this will clear monitor list and peer list.
        Usage in prompt: peer leavenet
    """

    def __init__(self, peer):
        super(LeaveNetCmd, self).__init__('leavenet')
        self.peer = peer

    def onProcess(self, msg_arr):
        self.peer.handler_broadcast_packet(
            host=('', 'all'), pkt_type=DisconnectHandler.pkt_type)
        self.peer.peer_pool = {}
        self.peer.logger.info('You left net.')
