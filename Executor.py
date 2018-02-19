import re
from Explainer import Explainer
from enums.SwitchMode import SwitchMode

class Executor:

    def __init__(self, sshClient=None):
        self.sshClient = sshClient

    def _mode_(self):
        self.mode = SwitchMode.ENABLE if re.compile('#$').search(self.sshClient.output[2:].decode('utf-8')) else SwitchMode.DEFAULT

    def _execute_(self, cmdInstance, short=True, debug=False):
        if debug:
            print('Mode: %s, Command: %s' % (str(self.mode), cmdInstance))
        return cmdInstance._execute_(self, short=short, debug=debug)
