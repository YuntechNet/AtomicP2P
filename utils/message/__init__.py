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

    def __init__(self, peer, can_broadcast=False):
        self.peer = peer
        self.can_broadcast = can_broadcast

    # Wrap if it is a broadcast packet.
    def wrap_packet(self, target, _type, _data, **kwargs):
        arr = []
        if self.can_broadcast and target[0] == 'broadcast':
            for each in self.peer.connectlist:
                if target[1] == 'all' or each.role == target[1]:
                    arr.append(Message(_host=each.host, _type=_type, _data=_data))
        else:
            arr.append(Message(_host=target, _type=_type, _data=_data))
        return arr

    def onSend(self, **kwargs):
        raise NotImplementedError

    def onRecv(self, **kwargs):
        raise NotImplementedError

