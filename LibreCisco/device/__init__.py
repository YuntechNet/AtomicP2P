from LibreCisco.utils.manager import ProcManager
from LibreCisco.device.command import AddCmd, RemoveCmd


class DeviceManager(ProcManager):

    def __init__(self, peer, loopDelay=1, output_field=None):
        super(DeviceManager, self).__init__(loopDelay=loopDelay,
                                            output_field=output_field)
        self.peer = peer
        self.devices = {}

    def registerHandler(self):
        pass

    def registerCommand(self):
        self.peer.handlers.update({
            'add': JoinHandler(self.peer, self),
            'remove': RemoveHandler(self.peer, self)
        })

    def onProcess(self, msg_arr, **kwargs):
        msg_key = msg_arr[0].lower()
        msg_arr = msg_arr[1:]
        if msg_key in self.commands:
            return self.commands[msg_key].onProcess(msg_arr)
        return ''

    def run(self):
        while not self.stopped.wait(self.loopDelay):
            pass
