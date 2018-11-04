import re
from pysnmp.hlapi.asyncore import *


class DeviceInfo(object):

    @staticmethod
    def snmp_v3_init(conn):
        outputs = conn.get_output(oid=[
                    ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName', 0)),
                    ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0))])
        hostname = outputs[0][outputs[0].rindex(' ') + 1:]
        version = re.compile('Version .*?,').search(outputs[1]).group(0)[8:-1]
        return DeviceInfo(version=version, hostname=hostname)

    @staticmethod
    def fromString(string):
        print(string)
        version = re.search('version .*?\n', string).group(0)[8:-2]
        hostname = re.search('hostname .*?\n', string).group(0)[9:-2]
        return DeviceInfo(version=version, hostname=hostname)

    def __init__(self, version, hostname):
        self.version = version
        self.hostname = hostname

    def __str__(self):
        return 'DeviceInfo<version={}, hostname={}>'.format(self.version,
                                                            self.hostname)
