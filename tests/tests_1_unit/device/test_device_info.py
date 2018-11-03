from LibreCisco.device.device_info import DeviceInfo


def test_init(test_device_info):
    assert test_device_info.version == 'test_version'
    assert test_device_info.hostname == 'test_hostname'


def test_str(test_device_info):
    assert str(test_device_info) == \
        'DeviceInfo<version={}, hostname={}>'.format('test_version',
                                                    'test_hostname')


def test_fromString():
    string = 'version test_version\r\n' \
             'hostname test_hostname\r\n'
    device_info = DeviceInfo.fromString(string=string)
    assert device_info.version == 'test_version'
    assert device_info.hostname == 'test_hostname'
