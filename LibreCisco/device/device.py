from LibreCisco.device.device_info import DeviceInfo
from LibreCisco.device.interface import Interface
from LibreCisco.device.connection import TelnetConnection, SSHConnection


class Device(object):

    def __init__(self, connect_type, host, account, passwd):
        self.authentication = {
            'connect_type': connect_type,
            'host': host,
            'account': account,
            'passwd': passwd
        }
        if connect_type == 'ssh':
            self.connection = SSHConnection(host=host, username=account,
                                            password=passwd)
        elif connect_type == 'telnet':
            self.connection = TelnetConnection(host=host, username=account,
                                               password=passwd)
        self.info = None
        self.interfaces = []

    def fetch_running_config(self):
        self.connection.login()
        output = self.connection.send_commands(
                       commands=['show run'], time_sleep=2, short=False)
        self.connection.logout()
        self.info = DeviceInfo.fromString(string=output)
        return output

    def fetch_interface_status(self):
        self.connection.login()
        output = self.connection.send_commands(
                       commands=['show interface status'], short=False)
        self.connection.logout()
        self.interfaces = Interface.fromString(string=output)
        return output

    def __str__(self):
        return 'Device<connect_type={}, host={}>'.format(
                    self.connect_type, self.authentication['host'])
