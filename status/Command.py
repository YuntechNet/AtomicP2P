
from network.commands.Command import Command
from status.commands.Online import Online
from status.commands.Status import Status
from status.commands.HeartBeat import HeartBeat

class StatusCommand:

    @staticmethod
    def processCheck(command):
        prefix = ['--status', 'status', 'heart-beat']
        for each in prefix:
            if each in command:
                return True
        return False

    @staticmethod
    def processRes(redis, command):
        if 'online' in command._command:
            Online.res(redis, command)
        elif 'status' in command._command:
            Status.res(redis, command)
        elif 'heart-beat' in command._command:
            HeartBeat.res(redis, command)

    @staticmethod
    def processReq(redis, _to, _command, _data):
        if 'online' in _command:
            Online.req(redis, _to, _data)
        elif 'status' in _command:
            Status.req(redis, _to, _data)
        elif 'heart-beat' in _command:
            HeartBeat.req(redis, _to, _data)

