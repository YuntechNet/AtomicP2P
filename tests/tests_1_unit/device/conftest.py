import pytest
from LibreCisco.device.interface import Interface
from LibreCisco.device.device_info import DeviceInfo
from LibreCisco.device.connection import SSHConnection, TelnetConnection


@pytest.fixture(scope='session')
def test_interface():
    return Interface(name='test_interface')


@pytest.fixture(scope='session')
def test_device_info():
    return DeviceInfo(model='test_model', version='test_version',
                      hostname='test_hostname')


@pytest.fixture(scope='session')
def ssh():
    host = ('127.0.0.1', 7022)
    account = 'root'
    passwd = 'toor'
    authentication = {
        'host': host,
        'account': account,
        'password': passwd
    }
    return SSHConnection(authentication=authentication)


@pytest.fixture(scope='session')
def telnet():
    host = ('127.0.0.1', 7023)
    account = 'root'
    passwd = 'toor'
    authentication = {
        'host': host,
        'account': account,
        'password': passwd
    }
    return TelnetConnection(authentication=authentication)
