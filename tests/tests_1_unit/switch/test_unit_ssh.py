import time


def test_init(request, ssh):
    config = request.config
    host = config.getoption('--ssh-test-host').split(':')
    account = config.getoption('--ssh-account')
    passwd = config.getoption('--ssh-passwd')
    assert ssh.manager is None
    assert ssh.host == (host[0], int(host[1]))
    assert ssh.username == account
    assert ssh.password == passwd
    assert ssh.timeout == 60


def test_login(ssh):
    ssh.login()
    assert ssh.is_active()
