import json

class Task:

    def __init__(self, ask, rtn, content):
        self.ask = ask
        self.rtn = rtn
        self.content = content

    @staticmethod
    def parse(data):
        jsonDict = json.loads(data)
        return Task(jsonDict['ask'], jsonDict['rtn'], jsonDict['content'])

    def to(self):
        return { 'ask': self.ask, 'rtn': self.rtn, 'content': self.content }
