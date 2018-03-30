import json

from network.commands.Command import Command
from network.Command import Commander

class ExecuteScript(Command):

    def __init__(self, cmd):
        Command.__init__(self, cmd._from, cmd._to, cmd._command, cmd._data)

    def req(self):
        return self

    def res(self, INS):
        return self

class SwitchCommand(Commander):

    def __init__(self, instance):
        Commander.__init__(self, instance)

    def process(self, command):
        if not super(SwitchCommand, self).process(command):
            self.INS.redis.print('message from %s: %s' % (command._from, command._command))

    @staticmethod
    def processReq(redis, command):
        if not Commander.processReq(redis, command):
            cmdIns = None
            if 'execute-script' in command._command:
                cmdIns = ExecuteScript(command)

            if cmdIns:
                cmdIns.req().send(redis)
                return True
        return False
