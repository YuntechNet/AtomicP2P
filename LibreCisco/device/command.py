from LibreCisco.device.device import Device
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
                    " - list                                           "
                    "list all services in list.\n"
                    " - device add [ssh/telnet] [ip:port] [account] [passwor"
                    "d]\n   device add snmp [ip:port] [account] [password] ["
                    "link-level] [auth_protocol] [auth_passowrd] [priv_proto"
                    "col] [priv_password]\n"
                    "  add service.\n"
                    " - help [cmd]                                     "
                    "show help msg of sepecific command.")


class ListCmd(Command):
    """ListCmd
        list all services in list
        Usage in prompt: device list
    """

    def __init__(self, device):
        super(ListCmd, self).__init__('list')
        self.device = device
        self.peer = device.peer

    def onProcess(self, msg_arr):
        msg = ''
        hostname = msg_arr[0]
        for each in self.device.devices:
            if each.info.hostname == hostname:
                for every in each.interfaces:
                    msg = '{}\n{}'.format(msg, str(every))
        return msg


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
                       account=account, passwd=passwd,
                       snmpEngine=self.device._snmpEngine,
                       link_level=link_level, auth_protocol=auth_protocol,
                       auth_password=auth_password,
                       priv_protocol=priv_protocol,
                       priv_password=priv_password)
        else:
            host = host.split(':')
            device = Device(connect_type=msg_arr[0], host=(host[0], host[1]),
                            account=msg_arr[2], passwd=msg_arr[3])
        self.device.addDevice(device)
        return '{} added.'.format(device.info.hostname)


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
