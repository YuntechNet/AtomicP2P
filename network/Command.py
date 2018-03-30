import json

from network.commands.Command import Command
from network.commands.Message import Message
from network.commands.Online import Online
from network.commands.HeartBeat import HeartBeat
from network.commands.Shutdown import Shutdown

class Commander:

    def __init__(self, instance):
        self.INS = instance

    def process(self, command):
        if 'message' in command._command:
            Message.res(self.INS, command)
        elif 'online' in command._command:
            Online.res(self.INS, command)
        elif 'heart-beat' in command._command:
            HeartBeat.res(self.INS, command)
        elif 'shutdown' in command._command:
            Shutdown.res(self.INS, command)
        else:
            return False
        return True

    @staticmethod
    def processReq(redis, command):
        cmdIns = None
        if 'message' in command._command:
            cmdIns = Message.req(redis, command)
            return True
        elif 'online' in command._command:
            cmdIns = Online.req(redis, command)
            return True
        elif 'heart-beat' in command._command:
            cmdIns = HeartBeat.req(redis, command)
            return True
        elif 'shutdown' in command._command:
            cmdIns = Shutdown.req(redis, command)
            return True
        else:
            return False
        return True
