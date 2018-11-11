from LibreCisco.utils.command import Command


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
        Usage in prompt: peer join [ip:port]
    """

    def __init__(self, peer):
        super(JoinCmd, self).__init__('join')
        self.peer = peer

    def onProcess(self, msg_arr):
        addr = msg_arr[0].split(':')
        self.peer.sendMessage((addr[0], addr[1]), 'join')
        return 'Joinning...'


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
        self.peer.sendMessage((addr[0], addr[1]), 'message', **mes)


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
        # self.peer.sendMessage(('broadcast', 'all'), 'leavenet')
        self.peer.connectlist.clear()
        self.peer.monitor.monitorlist.clear()
        return 'You left net.'
