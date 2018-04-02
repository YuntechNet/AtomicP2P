
from network.commands.Command import Command
from switch.commands.List import List
from switch.commands.ExecuteScript import ExecuteScript

class SwitchCommand:

    @staticmethod
    def processRes(redis, command):
        if 'ls' in command._command:
            List.res(redis, command)
        elif 'execute-script' in command._command:
            ExecuteScript.res(redis, command)

    @staticmethod
    def processReq(redis, _to, _command, _data):
        if 'ls' in _command:
            List.req(redis, _to, _data)
        elif 'execute-script' in _command:
            ExecuteScript.req(redis, _to, _data)

