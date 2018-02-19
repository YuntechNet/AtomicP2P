import re
from commands.Show import Show

class SwitchConfig:

    def __init__(self, switch):
        self.switch = switch
        self.loadConfig()
        
    def loadConfig(self):
        self.switch.sshClient.login()
        self.switch.executor._mode_()
        (self.switch.executor, result) = self.switch.executor._execute_(Show('run'), short=False)
        self.switch.sshClient.logout()
        self.hostname = re.compile('!\\r\\nhostname .*\\r\\n!').search(result).group(0)[12:-3]
        print(result)
