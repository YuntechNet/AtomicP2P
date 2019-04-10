import pytest
from LibreCisco.device.connection import SSHConnection, TelnetConnection


@pytest.fixture(scope='session')
def ssh(request):
    config = request.config
    host = config.getoption('--ssh-test-host').split(':')
    account = config.getoption('--ssh-account')
    passwd = config.getoption('--ssh-passwd')
    authentication = {
        'host': host,
        'account': account,
        'password': passwd
    }
    return SSHConnection(authentication=authentication)


@pytest.fixture(scope='session')
def telnet(request):
    config = request.config
    host = config.getoption('--telnet-test-host')
    account = config.getoption('--telnet-account')
    passwd = config.getoption('--telnet-passwd')
    authentication = {
        'host': host,
        'account': account,
        'password': passwd
    }
    return TelnetConnection(authentication=authentication)
