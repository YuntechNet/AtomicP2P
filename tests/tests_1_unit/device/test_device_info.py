from atomic_p2p.device.device_info import DeviceInfo


def test_init(test_device_info):
    assert test_device_info.model == 'test_model'
    assert test_device_info.version == 'test_version'
    assert test_device_info.hostname == 'test_hostname'


def test_str(test_device_info):
    assert str(test_device_info) == \
        'DeviceInfo<model={}, hostname={}>'.format(
            'test_model', 'test_hostname')


def test_fromString():
    string = 'model test_model\n'\
             'version test_version\r\n' \
             'hostname test_hostname\r\n'
    device_info = DeviceInfo.fromString(string=string)
    assert device_info.model == 'test_model'
    assert device_info.version == 'test_version'
    assert device_info.hostname == 'test_hostname'
