import re
from pysnmp.hlapi.asyncore import *


class Interface(object):

    @staticmethod
    def snmp_v3_init(conn):
        interfaces = []
        outputs = conn.get_output(oid=[
                         ObjectType(ObjectIdentity('IF-MIB', 'ifNumber', 0))])
        inter_count = int(outputs[0][outputs[0].rindex(' ') + 1:])
        outputs = conn.bulk_output(oid_with_NR=[
          (ObjectType(ObjectIdentity('IF-MIB', 'ifDescr')), (0, inter_count))])
        for each in outputs[:-1]:
            snmp_index = each[each.index('ifDescr.') + 8:each.rindex(' = ')]
            name = each[each.rindex(' ') + 1:]

            output = conn.get_output(oid=[
             ObjectType(ObjectIdentity('IF-MIB', 'ifOperStatus', snmp_index))])
            status = output[0][output[0].rindex(' ') + 1:]
            interfaces.append(Interface(snmp_index=snmp_index, name=name,
                                        status=status))
        return interfaces

    @staticmethod
    def fromReString(re_str):
        name = re_str[:re_str.index(' ')]
        return Interface(name=name)

    @staticmethod
    def fromString(string):
        interfaces = []
        for each in string.split('\n'):
            if 'connected' in each or 'notconnect' in each:
                interfaces.append(Interface.fromReString(re_str=each))
        return interfaces

    def __init__(self, name, status=None, snmp_index=-1):
        self.name = name
        self.status = status
        self.snmp_index = int(snmp_index)

    def __str__(self):
        return 'Interface<snmp_index={}, name={}, status={}>'.format(
            self.snmp_index, self.name, self.status)
