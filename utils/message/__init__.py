import json


class Message(object):

    def __init__(self, _host, _type, _data):
        if type(_host[1]) != int:
            self._host = (_host[0], int(_host[1]))
        else:
            self._host = _host
        self._type = _type
        self._data = _data

    def __str__(self):
        return 'Message<>'

    def toDict(self):
        return {
            'host': {
                'ip': self._host[0],
                'port': int(self._host[1])
            },
            'type': self._type,
            'data': self._data
        }

    @staticmethod
    def recv(data):
        data = json.loads(str(data, encoding='utf-8'))
        return Message((data['host']['ip'], data['host']['port']), data['type'], data['data'])

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

