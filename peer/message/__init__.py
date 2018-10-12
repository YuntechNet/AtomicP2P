import json


class Message(object):

    def __init__(self, _ip, _type, _data):
        if type(_ip[1]) != int:
            self._ip = (_ip[0], int(_ip[1]))
        else:
            self._ip = _ip
        self._type = _type
        self. _data = _data

    def toDict(self):
        return {
            'ip': {
                'host': self._ip[0],
                'port': int(self._ip[1])
            },
            'type': self._type,
            'data': self._data
        }

    @staticmethod
    def recv(data):
        data = json.loads(str(data, encoding='utf-8'))
        return Message((data['ip']['host'], data['ip']['port']), data['type'], data['data'])

    @staticmethod
    def send(data):
        data = json.dumps(data.toDict())
        return bytes(data, encoding='utf-8')

class Handler(object):

    def __init__(self, peer):
        self.peer = peer

    def onSend(self, **kwargs):
        raise NotImplementedError

    def onRecv(self, **kwargs):
        raise NotImplementedError
