

def test_send_command(ssh):
    ssh.login()
    assert ssh.is_active() is True
    ssh.logout()
    assert ssh.is_active() is False
