from LibreCisco.device.device import Device
from LibreCisco.utils.command import Command


class ListCmd(Command):
    """ListCmd
        list all services in list
        Usage in prompt: device list
    """

    def __init__(self, device):
        super(ListCmd, self).__init__('list')
        self.device = device
        self.peer = device.peer
        self.output_field = self.device.output_field

    def onProcess(self, msg_arr):
        pass


class AddCmd(Command):
    """AddCmd
        add service.
        Usage in prompt: device add [ssh/telnet] [ip:port] [account] [password]
    """

    def __init__(self, device):
        super(AddCmd, self).__init__('add')
        self.device = device
        self.peer = device.peer
        self.output_field = self.device.output_field

    def onProcess(self, msg_arr):
        host = msg_arr[1].split(':')
        device = Device(connect_type=msg_arr[0], host=(host[0], host[1]),
                        account=msg_arr[2], passwd=msg_arr[3])
        self.device.addDevice(device)


class RemoveCmd(Command):
    """
        Command to remove a device.
    """

    def __init__(self, device):
        super(RemoveCmd, self).__init__('remove')
        self.device = device
        self.peer = device.peer

    def onProcess(self, msg_arr):
        pass
