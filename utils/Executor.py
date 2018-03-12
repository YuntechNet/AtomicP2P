import re
from utils.Explainer import Explainer
from utils.Enums import SwitchMode

# Executor
#   Class definition store executing status of switch.
#
class Executor:

    def __init__(self, sshClient=None):
        self.sshClient = sshClient

    # Before execute any command, have to get switch's operating mode first.
    def _mode_(self):
        self.mode = SwitchMode.ENABLE if re.compile('#$').search(self.sshClient.output[2:].decode('utf-8')) else SwitchMode.DEFAULT

    def _execute_(self, cmdInstance, short=True, debug=False):
        if debug:
            print('Mode: %s, Command: %s' % (str(self.mode), cmdInstance))
        return cmdInstance._execute_(self, short=short, debug=debug)

    def _executeStr_(self, cmdString, short=True, wrap=True, debug=False):
        self.sshClient.sendCommand(cmdString, wrap=wrap)
        result = self.sshClient.shell.recv(65535).decode('utf-8')
        while('#' not in result and '>' not in result):
            if ' --More--' in result:
                result = result.replace(' --More-- ', '') + self.sshClient.send_command('q' if short else ' ', wrap=False)
            elif self.sshClient.isActive():
                result += self.sshClient.shell.recv(65535).decode('utf-8')
            else:
                break
        if debug:
            print(result)
        return (self, result)
