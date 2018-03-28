import json

class Command:

    def __init__(self, _from, _to, _content, _data=None):
        self._from = _from
        self._to = _to
        self._content = _content
        self._data = _data
    
    @staticmethod
    def parse(data):
        jsonDict = json.loads(data)
        return Command(jsonDict['_from'], jsonDict['_to'], jsonDict['_content'], jsonDict['_data'])

    def to(self):
        return json.dumps({ '_from': self._from, '_to': self._to, '_content': self._content, '_data': self._data })
    
    def send(self, redis):
        redis.pub(self._to, self.to())

    def swap(self):
        temp = self._from
        self._from = self._to
        self._to = temp

class Online(Command):

    def __init__(self, cmd):
        Command.__init__(self, cmd._from, cmd._to, cmd._content)

    def req(self):
        return self

    def res(self, INS):
        self.swap()
        self._content = 'I\'m online bitch!'
        return self

class HeartBeat(Command):

    def __init__(self, cmd):
        Command.__init__(self, cmd._from, cmd._to, cmd._content)

    def req(self):
        return self

    def res(self, INS):
        INS.redis.print('%s is checking am i dead, but i\'m cooooooooool.' % self._from)
        self.swap()
        self._content = 'I\'m still alive. jerk!'
        return self

class Shutdown(Command):

    def __init__(self, cmd):
        Command.__init__(self, cmd._from, cmd._to, cmd._content)

    def req(self):
        return self

    def res(self, INS):
        return self

class Commander:

    def __init__(self, instance):
        self.INS = instance

    def process(self, command):
        if 'online' in command._content:
            Online(command).res(self.INS).send(self.INS.redis)
        elif 'heart-beat' in command._content:
            HeartBeat(command).res(self.INS).send(self.INS.redis)
        elif 'shutdown' in command._content:
            Shutdown(command).res(self.INS).send(self.INS.redis)
        else:
            return False
        return True

    @staticmethod
    def processReq(redis, command):
        cmdIns = None
        if 'online' in command._content:
            cmdIns = Online(command)
        elif 'heart-beat' in command._content:
            cmdIns = HeartBeat(command)
        elif 'shutdown' in command._content:
            cmdIns = Shutdown(command)

        if cmdIns:
            cmdIns.req().send(redis)
            return True
        return False
