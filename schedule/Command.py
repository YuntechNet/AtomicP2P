import re

from network.Command import Command, Commander
from utils.Enums import CommandType

class List(Command):

    def __init__(self, cmd):
        Command.__init__(self, cmd._from, cmd._to, cmd._command)

    def req(self):
        return self

    def res(self, INS):
        argv = self._command.replace('ls', '').split(' ')
        if not argv == ['']:
            for (key, value) in INS.schedules.items():
                if key in argv:
                    value.info()
        else:
            [INS.print(value.info()) for (key, value) in INS.schedules.items()]
        self.swap()
        self._command = 'Got you bitch!'
        return self

class LoadFolder(Command):

    def __init__(self, cmd):
        Command.__init__(self, cmd._from, cmd._to, cmd._command)

    def req(self):
        return self

    def res(self, INS):
        argv = self._command.replace('load-folder', '').split(' ')
        path = re.compile('-path=.*?.json', re.DOTALL).search(self._command)
        INS.loadFolder(path=path.group(0)[6:] if path else None, overwrite='-force' in argv, immediate='-immediate' in argv)
        self.swap()
        self._command = 'Done~~~'
        return self

class Start(Command):

    def __init__(self, cmd):
        Command.__init__(self, cmd._from, cmd._to, cmd._command)

    def req(self):
        return self

    def res(self, INS):
        argv = self._command.replace('start', '').split(' ')
        if not argv == ['']:
            for (key, value) in INS.schedules.items():
                if key in argv:
                    value.start()
        else:
            [value.start() for (key, value) in INS.schedules.items()]
        self.swap()
        self._command = 'DONE START'
        return self

class Stop(Command):

    def __init__(self, cmd):
        Command.__init__(self, cmd._from, cmd._to, cmd._command)

    def req(self):
        return self

    def res(self, INS):
        argv = self._command.replace('stop', '').split(' ')
        if not argv == ['']:
            for (key, value) in INS.schedules.copy().items():
                if key in argv:
                    value.exit()
        else:
            [value.exit() for (key, value) in INS.schedules.items()]
            INS.schedules.clear()
        self.swap()
        self._command = 'DONE STOP'
        return self

class ScheduleCommand(Commander):

    def __init__(self, instance):
        Commander.__init__(self, instance)

    def process(self, command):
        if not super(ScheduleCommand, self).process(command):
            if 'ls' in command._command:
                List(command).res(self.INS).send(self.INS.redis)
            elif 'load-folder' in command._command:
                LoadFolder(command).res(self.INS).send(self.INS.redis)
            elif 'start' in command._command:
                Start(command).res(self.INS).send(self.INS.redis)
            elif 'stop' in command._command:
                Stop(command).res(self.INS).send(self.INS.redis)
            else:
                self.INS.redis.print('message from %s: %s' % (command._from, command._command))

    @staticmethod
    def processReq(redis, command):
        if not Commander.processReq(redis, command):
            cmdIns = None
            if 'ls' in command._command:
                cmdIns = List(command)
            elif 'load-folder' in command._command:
                cmdIns = LoadFolder(command)
            elif 'start' in command._command:
                cmdIns = Start(command)
            elif 'stop' in command._command:
                cmdIns = Stop(command)
        
            if cmdIns:
                cmdIns.req().send(redis)
                return True
        return False

