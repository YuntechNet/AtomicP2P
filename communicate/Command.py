import json

class Command:

    def __init__(self, _from, _to, _content):
        self._from = _from
        self._to = _to
        self._content = _content
    
    @staticmethod
    def parse(data):
        jsonDict = json.loads(data)
        return Command(jsonDict['_from'], jsonDict['_to'], jsonDict['_content'])

    def to(self):
        return json.dumps({ '_from': self._from, '_to': self._to, '_content': self._content })
