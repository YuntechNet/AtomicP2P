import json


class Message(object):

    def __init__(self, _to, _from, _hash, _type, _data):
        if type(_to[1]) != int or type(_from[1]) != int:
            self._to = (_to[0], int(_to[1]))
            self._from = (_from[0], int(_from[1]))
        else:
            self._to = _to
            self._from = _from
        self._hash = _hash
        self._type = _type
        self._data = _data

    def __str__(self):
        return 'Message<>'

    def set_reject(self, reject, maintain_data=False):
        if maintain_data:
            self._data['reject'] = reject
        else:
            self._data = {
                'reject': reject
            }

    def is_reject(self):
        return 'reject' in self._data

    def toDict(self):
        return {
            'to': {
                'ip': self._to[0],
                'port': self._to[1]
            },
            'from': {
                'ip': self._from[0],
                'port': self._from[1]
            },
            'hash': self._hash,
            'type': self._type,
            'data': self._data
        }

    @staticmethod
    def recv(data):
        data = json.loads(str(data, encoding='utf-8'))
        return Message(_to=(data['to']['ip'], data['to']['port']),
                       _from=(data['from']['ip'], data['from']['port']),
                       _hash=data['hash'], _type=data['type'],
                       _data=data['data'])

    @staticmethod
    def send(data):
        data = json.dumps(data.toDict())
        return bytes(data, encoding='utf-8')


class Handler(object):

    def __init__(self, peer, can_broadcast=False, can_reject=True):
        self.peer = peer
        self.can_broadcast = can_broadcast
        self.can_reject = can_reject

    # Wrap if it is a broadcast packet.
    def wrap_packet(self, target, _type, _data, **kwargs):
        arr = []
        if self.can_broadcast and target[0] == 'broadcast':
            for each in self.peer.connectlist:
                if target[1] == 'all' or each.role == target[1]:
                    arr.append(Message(_to=each.host, _from=self.peer.host,
                                       _hash=self.peer._hash, _type=_type,
                                       _data=_data))
        else:
            arr.append(Message(_to=target, _from=self.peer.host,
                               _hash=self.peer._hash, _type=_type,
                               _data=_data))
        return arr

    def onSend(self, target, **kwargs):
        if self.can_reject and 'reject' in locals()['kwargs']:
            return self.onSendReject(target=target,
                                     reason=kwargs['reject'], **kwargs)
        else:
            return self.onSendPkt(target=target, **kwargs)

    def onSendReject(self, target, reason, **kwargs):
        raise NotImplementedError

    def onSendPkt(self, target, **kwargs):
        raise NotImplementedError

    def onRecv(self, src, data, **kwargs):
        if self.can_reject and 'reject' in data:
            self.onRecvReject(src=src, data=data, **kwargs)
        else:
            self.onRecvPkt(src=src, data=data, **kwargs)

    def onRecvReject(self, src, data, **kwargs):
        raise NotImplementedError

    def onRecvPkt(self, src, data, **kwargs):
        raise NotImplementedError
