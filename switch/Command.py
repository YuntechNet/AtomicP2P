
from network.commands.Command import Command
from switch.commands.ExecuteScript import ExecuteScript

class SwitchCommand:

    @staticmethod
    def processRes(redis, command):
        if 'execute-script' in command._command:
            ExecuteScript.res(redis, command)

    @staticmethod
    def processReq(redis, command):
        if 'execute-script' in command._command:
            ExecuteScript.req(redis, command)

