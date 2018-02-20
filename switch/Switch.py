from ssh_switch import ssh_switch
from utils.Executor import Executor
from switch.SwitchConfig import SwitchConfig

class Switch:

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.sshClient = ssh_switch(host, username, password)
        self.executor = Executor(self.sshClient)
        self.config = SwitchConfig(self)
