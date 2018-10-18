

def test_sendCommand(ssh):
    ssh.login()
    assert ssh.is_active() is True
    ssh.sendCommand('\x08')
    ssh.sendCommand('\x0A')
    ssh.sendCommand('\x0A')
    ssh.sendCommand('exit')
    ssh.logout()
    assert ssh.is_active() is False


def test_send_command(ssh):
    ssh.login()
    assert ssh.is_active() is True
    ssh.send_command('\x08')
    ssh.send_command('\x0A')
    ssh.send_command('\x0A')
    ssh.send_command('exit')
    ssh.logout()
    assert ssh.is_active() is False
