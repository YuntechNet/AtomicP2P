

def test_sendCommand(telnet):
    telnet.login()
    assert telnet.is_active() is True
    telnet.logout()
    assert telnet.is_active() is False
