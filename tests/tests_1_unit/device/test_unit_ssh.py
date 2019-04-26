import time


def test_init(ssh):
    assert ssh.host == ('127.0.0.1', 7022)
    assert ssh.username == 'root'
    assert ssh.password == 'toor'
    assert ssh.timeout == 60


def test_login(ssh):
    ssh.login()
    assert ssh.is_active()
