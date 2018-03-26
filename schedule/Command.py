
from communicate.Command import Command, Commander
from utils.Enums import CommandType

class List(Command):

    def __init__(self, cmd):
        Command.__init__(self, cmd._from, cmd._to, cmd._content)

    def req(self):
        return self

    def res(self, INS):
        [INS.print('%s %s' % (key, value)) for (key, value) in INS.schedules.items()]
        self.swap()
        self._content = 'Got you bitch!'
        return self

class LoadFolder(Command):

    def __init__(self, cmd):
        Command.__init__(self, cmd._from, cmd._to, cmd._content)

    def req(self):
        return self

    def res(self, INS):
        INS.loadFolder(overwrite='-force' in self._content)
        self.swap()
        self._content = 'Done~~~'
        return self

class Start(Command):

    def __init__(self, cmd):
        Command.__init__(self, cmd._from, cmd._to, cmd._content)

    def req(self):
        return self

    def res(self, INS):
        [value.start() for (key, value) in INS.schedules.items()]
        return self

class Stop(Command):

    def __init__(self, cmd):
        Command.__init__(self, cmd._from, cmd._to, cmd._content)

    def req(self):
        return self

    def res(self, INS):
        [value.exit() for (key, value) in INS.schedules.items()]
        return self

class ScheduleCommand(Commander):

    def __init__(self, instance):
        Commander.__init__(self, instance)

    def process(self, command):
        if not super(ScheduleCommand, self).process(command):
            if 'ls' in command._content:
                List(command).res(self.INS).send(self.INS.redis)
            elif 'load-folder' in command._content:
                LoadFolder(command).res(self.INS).send(self.INS.redis)
            elif 'start' in command._content:
                Start(command).res(self.INS).send(self.INS.redis)
            elif 'stop' in command._content:
                Stop(command).res(self.INS).send(self.INS.redis)
            else:
                self.INS.redis.print('message from %s: %s' % (command._from, command._content))

    @staticmethod
    def processReq(redis, command):
        if not Commander.processReq(redis, command):
            cmdIns = None
            if 'ls' in command._content:
                cmdIns = List(command)
            elif 'load-folder' in command._content:
                cmdIns = LoadFolder(command)
            elif 'start' in command._content:
                cmdIns = Start(command)
            elif 'stop' in command._content:
                cmdIns = Stop(command)
        
            if cmdIns:
                cmdIns.req().send(redis)
                return True
        return False

