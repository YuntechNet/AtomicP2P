from atomic_p2p.device.interface import Interface


def test_init(test_interface):
    assert test_interface.name == 'test_interface'


def test_str(test_interface):
    assert str(test_interface) == \
            'Interface<snmp_index={}, name={}, status={}>'.format(
                -1, 'test_interface', None)


def test_fromReString():
    string = 'Fa0/1                        ' \
             'notconnect   1            auto   auto 10/100BaseTX'
    interface = Interface.fromReString(re_str=string)
    assert interface.name == 'Fa0/1'


def test_fromString():
    strings = 'Port      Name               Status       Vlan       Duplex' \
              '  Speed Type\n' \
              'Fa0/1                        notconnect   1            auto' \
              '   auto 10/100BaseTX\n' \
              'Fa0/2                        connected    1          a-full' \
              '  a-100 10/100BaseTX\n' \
              'Gi0/1                        notconnect   1            auto' \
              '   auto Not Present\n' \
              'Gi0/2                        notconnect   1            auto' \
              '   auto Not Present'
    interfaces = Interface.fromString(string=strings)
    assert len(interfaces) == 4
    assert interfaces[0].name == 'Fa0/1'
    assert interfaces[1].name == 'Fa0/2'
    assert interfaces[2].name == 'Gi0/1'
    assert interfaces[3].name == 'Gi0/2'
