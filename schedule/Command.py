
from network.commands.Command import Command
from schedule.commands.List import List
from schedule.commands.LoadFolder import LoadFolder
from schedule.commands.Start import Start
from schedule.commands.Stop import Stop

class ScheduleCommand:

    @staticmethod
    def processRes(redis, command):
        if 'ls' in command._command:
            List.res(redis, command)
        elif 'load-folder' in command._command:
            LoadFolder.res(redis, command)
        elif 'start' in command._command:
            Start.res(redis, command)
        elif 'stop' in command._command:
            Stop.res(redis, command)

    @staticmethod
    def processReq(redis, command):
        if 'ls' in command._command:
            List.req(redis, command)
        elif 'load-folder' in command._command:
            LoadFolder.req(redis, command)
        elif 'start' in command._command:
            Start.req(redis, command)
        elif 'stop' in command._command:
            Stop.req(redis, command)
        
