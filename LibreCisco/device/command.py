from LibreCisco.device.device import Device
from LibreCisco.utils import printText
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
        hostname = msg_arr[0]
        for each in self.device.devices:
            if each.info.hostname == hostname:
                for every in each.interfaces:
                    printText(str(every))


class AddCmd(Command):
    """AddCmd
        add service.
        Usage in prompt:
            device add [ssh/telnet] [ip:port] [account] [password]
            device add snmp [ip:port] [account] [password] [link-level] [auth_p
            rotocol] [auth_passowrd] [priv_protocol] [priv_password]
    """

    def __init__(self, device):
        super(AddCmd, self).__init__('add')
        self.device = device
        self.peer = device.peer
        self.output_field = self.device.output_field

    def onProcess(self, msg_arr):
        connect_type = msg_arr[0]
        host = msg_arr[1]
        account = msg_arr[2]
        passwd = msg_arr[3]
        if connect_type == 'snmp':
            link_level = msg_arr[4]
            auth_protocol = msg_arr[5]
            auth_password = msg_arr[6]
            priv_protocol = msg_arr[7]
            priv_password = msg_arr[8]
            device = \
                Device(connect_type=connect_type, host=(host, 161),
                       account=account, passwd=passwd, link_level=link_level,
                       auth_protocol=auth_protocol,
                       auth_password=auth_password,
                       priv_protocol=priv_protocol,
                       priv_password=priv_password)
        else:
            host = host.split(':')
            device = Device(connect_type=msg_arr[0], host=(host[0], host[1]),
                            account=msg_arr[2], passwd=msg_arr[3])
        self.device.addDevice(device)
        printText(device.info.hostname + ' added.')


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
