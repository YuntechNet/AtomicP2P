def pytest_addoption(parser):
    parser.addoption('--ssh-test-host', action='store', default=None)
    parser.addoption('--ssh-account', action='store', default=None)
    parser.addoption('--ssh-passwd', action='store', default=None)
    parser.addoption('--telnet-test-host', action='store', default=None)
    parser.addoption('--telnet-account', action='store', default=None)
    parser.addoption('--telnet-passwd', action='store', default=None)
