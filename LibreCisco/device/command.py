from LibreCisco.utils.command import Command


class AddCmd(Command):
    """
        Command to add devices.
    """

    def __init__(self, peer, device):
        super(AddCmd, self).__init__('add')
        self.peer = peer
        self.device = device

    def onProcess(self, msg_arr):
        pass

class RemoveCmd(Command):
    """
        Command to remove a device.
    """

    def __init__(self, peer, device):
        super(RemoveCmd, self).__init__('remove')
        self.peer = peer
        self.device = device

    def onProcess(self, msg_arr):
        pass 
