import json

class Command:

    def __init__(self, _from, _to, _command, _data=None):
        self._from = _from
        self._to = _to
        self._command = _command
        self._data = _data
    
    @staticmethod
    def parse(data):
        jsonDict = json.loads(data)
        c = Command(None, jsonDict['_to'], jsonDict['_command'], jsonDict['_data'])
        c._from = jsonDict['_from']
        return c

    def to(self):
        return json.dumps({ '_from': self._from, '_to': self._to, '_command': self._command, '_data': self._data })
    
    def send(self, redis):
        self._from = redis.name
        redis.pub(self._to, self.to())

    def swap(self):
        temp = self._from
        self._from = self._to
        self._to = temp
        return self
