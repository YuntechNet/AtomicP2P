import re
from pysnmp.hlapi.asyncore import *


class DeviceInfo(object):

    @staticmethod
    def snmp_v3_init(conn):
        outputs = conn.get_output(oid=[
                    ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName', 0)),
                    ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0))])
        model = re.compile('Software, .*? Software').search(outputs[1]).group(0)[10:-9]
        hostname = outputs[0][outputs[0].rindex(' ') + 1:]
        version = re.compile('Version .*?,').search(outputs[1]).group(0)[8:-1]
        return DeviceInfo(model=model, version=version, hostname=hostname)

    @staticmethod
    def fromString(string):
        print(string)
        model = re.compile('model .*?\n').search(string).group(0)[6:-1]
        version = re.search('version .*?\n', string).group(0)[8:-2]
        hostname = re.search('hostname .*?\n', string).group(0)[9:-2]
        return DeviceInfo(model=model, version=version, hostname=hostname)

    def __init__(self, model, version, hostname):
        self.model = model
        self.version = version
        self.hostname = hostname

    def __str__(self):
        return 'DeviceInfo<model={}, hostname={}>'.format(self.model,
                                                          self.hostname)
