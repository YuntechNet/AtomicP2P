
from utils import printText
from utils.command import Command

class SendCmd(Command):

    def __init__(self, peer, **kwargs):
        super(SendCmd, self).__init__('send')
        self.peer = peer

    def onProcess(self, msg_arr, **kwargs):
        msg_key = msg_arr[0]
        msg_arr = msg_arr[1:]
        addr = msg_key.split(':')
        mes = {'msg': msg_arr}
        self.peer.sendMessage((addr[0], addr[1]),'message', **mes)

class BroadcastCmd(Command):

    def __init__(self, peer, **kwargs):
        super(BroadcastCmd, self).__init__('broadcast')
        self.peer = peer

    def onProcess(self, msg_arr, **kwargs):
        msg_key = msg_arr[0]
        msg_arr = msg_arr[1:]
        data = {
            'role': msg_key,
            'msg': msg_arr
        }
        for member in self.peer.connectlist:
            self.peer.sendMessage((member.host[0], member.host[1]), 'broadcast', **data)

class ListCmd(Command):

    def __init__(self, peer, **kwargs):
        super(ListCmd, self).__init__('list')
        self.peer = peer
        self.output_field = peer.output_field

    def onProcess(self, msg_arr, **kwargs):
        for each in self.peer.connectlist:
            printText(each)

