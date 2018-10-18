

def test_sendCommand(telnet):
    telnet.login()
    assert telnet.is_active() is True
    telnet.sendCommand('\x08')
    telnet.sendCommand('\x0A')
    telnet.sendCommand('\x0A')
    telnet.sendCommand('exit')
    telnet.logout()
    assert telnet.is_active() is False
