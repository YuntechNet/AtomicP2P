import json

from Config import Config
from ssh_switch import ssh_switch
from utils.Executor import Executor
from utils.Lock import Lock
from switch.Config import SwitchConfig

from commands.Show import Show

class Switch:

    def __init__(self, config):
        self.host = config['host']
        self.username = config['username'] if 'username' in config else Config.SWITCH_MANAGER['DEFAULT_USERNAME']
        self.password= config['password'] if 'password' in config else Config.SWITCH_MANAGER['DEFAULT_PASSWORD']
        self.sshClient = ssh_switch(self.host, self.username, self.password)
        self.executor = Executor(self.sshClient)
        self.config = SwitchConfig(self)
        self.lock = Lock()

    def singleExecute(self, operator, singleCommand, short=True, safe=True, timeout=60):
        if self.lock.isLock():
            print('Switch is locked, using by: %s' % self.lock.getLocker())
            return

        if safe:
            self.lock.setLock(operator)

        self.sshClient.login(timeout=timeout)
        self.executor._mode_()
        (self.executor, result) = self.executor._execute_(singleCommand, short)
        self.sshClient.logout()

        if safe:
            self.lock.unLock()
        return result

    def stageExecute(self, operator, listCommand, short=True, safe=True, timeout=60):
        if self.lock.isLock():
            print('Switch is locked, using by: %s' % self.lock.getLovkc())
            return

        if safe:
            self.lock.setLock(operator)

        self.sshClient.login(timeout=timeout)
        self.executor._mode_()
        for singleCommand in listCommand:
            (self.executor, resultSingle) = self.executor._execute_(singleCommand, short)
            result += resultSingle
        self.sshClient.logout()

        if safe:
            self.lock.unLock()
        return result

    def initSwitch(self, debug=False):
        #self.config.loadConfig(debug)
        self.config.loadNeighbor(debug)

