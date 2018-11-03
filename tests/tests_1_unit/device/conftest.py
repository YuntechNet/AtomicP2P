import pytest
from LibreCisco.device.interface import Interface
from LibreCisco.device.device_info import DeviceInfo
from LibreCisco.device.connection import SSHConnection, TelnetConnection


@pytest.fixture(scope='session')
def test_interface():
    return Interface(name='test_interface')


@pytest.fixture(scope='session')
def test_device_info():
    return DeviceInfo(version='test_version', hostname='test_hostname')


@pytest.fixture(scope='session')
def ssh(request):
    config = request.config
    host = config.getoption('--ssh-test-host').split(':')
    account = config.getoption('--ssh-account')
    passwd = config.getoption('--ssh-passwd')
    return SSHConnection(host=host, username=account, password=passwd)


@pytest.fixture(scope='session')
def telnet(request):
    config = request.config
    host = config.getoption('--telnet-test-host').split(':')
    account = config.getoption('--telnet-account')
    passwd = config.getoption('--telnet-passwd')
    return TelnetConnection(host=host, username=account, password=passwd)
