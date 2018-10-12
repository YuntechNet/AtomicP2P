import json


class Message(object):

    def __init__(self, _ip, _type, _data):
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
        data = json.loads(data)
        return Message((data['ip']['host'], data['ip']['port']), data['type'], data['data'])

    @staticmethod
    def send(data):
        data = json.dumps(data.toDict())
        return data

class Handler(object):

    def __init__(self, peer):
        self._peer = peer

    def onSend(self, **kwargs):
        raise NotImplementedError

    def onRecv(self, **kwargs):
        raise NotImplementedError

