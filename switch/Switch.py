from Config import Config
from ssh_switch import ssh_switch
from utils.Executor import Executor
from switch.SwitchConfig import SwitchConfig

class Switch:

    def __init__(self, configDict):
        self.host = configDict['host']
        self.username = configDict['username'] if 'username' in configDict else Config.DEFAULT_DEVICE_LOGIN_USERNAME
        self.password= configDict['password'] if 'password' in configDict else Config.DEFAULT_DEVICE_LOGIN_PASSWORD
        self.sshClient = ssh_switch(self.host, self.username, self.password)
        self.executor = Executor(self.sshClient)
        self.config = SwitchConfig(self)

    def initSwitch(self):
        self.config.loadConfig()
