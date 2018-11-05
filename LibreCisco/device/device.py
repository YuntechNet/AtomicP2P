from LibreCisco.device.device_info import DeviceInfo
from LibreCisco.device.interface import Interface
from LibreCisco.device.connection import (
    SNMPv3Connection as SNMPv3Conn, TelnetConnection as TelnetConn,
    SSHConnection as SSHConn
)


class Device(object):

    def __init__(self, connect_type, host, account, passwd, link_level=None,
                 auth_protocol=None, priv_protocol=None, auth_password=None,
                 priv_password=None):
        self.authentication = \
            self.create_authentication(
                connect_type=connect_type, host=host, link_level=link_level,
                account=account, password=passwd,
                auth_protocol=auth_protocol, auth_password=auth_password,
                priv_protocol=priv_protocol, priv_password=priv_password)
        self.connect_type = connect_type
        if connect_type == 'snmp':
            self.connection = SNMPv3Conn(authentication=self.authentication)
        else:
            self.connection = SSHConn(authentication=self.authentication) if \
                              connect_type == 'ssh' else \
                              TelnetConn(authentication=self.authentication)
        self.info = None
        self.interfaces = []

    def create_authentication(self, connect_type, host, account, password=None,
                              link_level=None, auth_protocol=None,
                              priv_protocol=None, auth_password=None,
                              priv_password=None):
        authentication = {
            'connect_type': connect_type,
            'host': host,
            'account': account
        }
        if connect_type == 'ssh' or connect_type == 'telnet':
            authentication['password'] = password
        elif connect_type == 'snmp':
            authentication['link_level'] = link_level
            authentication['auth_protocol'] = auth_protocol
            authentication['priv_protocol'] = priv_protocol
            authentication['auth_password'] = auth_password
            authentication['priv_password'] = priv_password
        return authentication

    def snmp_v3_init(self):
        self.info = DeviceInfo.snmp_v3_init(conn=self.connection)
        self.interfaces = Interface.snmp_v3_init(conn=self.connection)

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
