import json

from Config import Config
from ssh_switch import ssh_switch
from utils.Executor import Executor
from switch.Config import SwitchConfig

class Switch:

    def __init__(self, config):
        self.host = config['host']
        self.username = config['username'] if 'username' in config else Config.SWITCH_MANAGER['DEFAULT_USERNAME']
        self.password= config['password'] if 'password' in config else Config.SWITCH_MANAGER['DEFAULT_PASSWORD']
        self.sshClient = ssh_switch(self.host, self.username, self.password)
        self.executor = Executor(self.sshClient)
        self.config = SwitchConfig(self)

    def initSwitch(self):
        self.config.loadConfig()
