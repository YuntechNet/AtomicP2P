import json

from network.commands.Command import Command
from network.commands.Message import Message
from network.commands.Online import Online
from network.commands.HeartBeat import HeartBeat
from network.commands.Shutdown import Shutdown

from core.Command import LibCiscoCommand
from switch.Command import SwitchCommand
from schedule.Command import ScheduleCommand
from server.Command import LibServerCommand

class Commander:

    @staticmethod
    def processRes(redis, command):
        if 'message' in command._command:
            Message.res(redis, command)
        elif 'online' in command._command:
            Online.res(redis, command)
        elif 'heart-beat' in command._command:
            HeartBeat.res(redis, command)
        elif 'shutdown' in command._command:
            Shutdown.res(redis, command)
        elif '--libcisco' in command._command:
            LibCiscoCommand.processRes(redis, command)
        elif '--switch' in command._command:
            SwitchCommand.processRes(redis, command)
        elif '--schedule' in command._command:
            ScheduleCommand.processRes(redis, command)
        elif '--libserver' in command._command:
            LibServerCommand.processRes(redis, command)

    @staticmethod
    def processReq(redis, command):
        if 'message' in command._command:
            Message.req(redis, command)
        elif 'online' in command._command:
            Online.req(redis, command)
        elif 'heart-beat' in command._command:
            HeartBeat.req(redis, command)
        elif 'shutdown' in command._command:
            Shutdown.req(redis, command)
        elif '--libcisco' in command._command:
            LibCiscoCommand.processReq(redis, command)
        elif '--switch' in command._command:
            SwitchCommand.processReq(redis, command)
        elif '--schedule' in command._command:
            ScheduleCommand.processReq(redis, command)
        elif '--libserver' in command._command:
            LibServerCommand.processReq(redis, command)
        else:
            pass
