from LibreCisco.utils import printText
from LibreCisco.utils.command import Command


class SendCmd(Command):
    """SendCmd
        send a message to a specific peer or broadcast in prompt.
        Usage in prompt: peer send [host/broadcast:all] [msg]
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
        self.output_field = peer.output_field

    def onProcess(self, msg_arr):
        if len(self.peer.connectlist) == 0:
            printText('There is no peers in current net.')
        else:
            printText('There is the list of peers in current net:')
            for each in self.peer.connectlist:
                printText(' - ' + str(each))
            printText('[---End of list---]')


class LeaveNetCmd(Command):
    """LeaveNetCmd
        leave the current net, this will clear watchdog list and peer list.
        Usage: peer leavenet
    """

    def __init__(self, peer):
        super(LeaveNetCmd, self).__init__('leavenet')
        self.peer = peer
        self.output_field = peer.output_field

    def onProcess(self, msg_arr):
        # self.peer.sendMessage(('broadcast', 'all'), 'leavenet')
        self.peer.connectlist.clear()
        self.peer.watchdog.watchdoglist.clear()
        printText('You left net.')
