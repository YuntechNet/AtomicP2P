import json
from LibreCisco.utils import printText


class Message(object):

    def __init__(self, _to, _from, _hash, _type, _data):
        self._to = _to
        self._from = _from
        self._hash = _hash
        self._type = _type
        self._data = _data

    def __str__(self):
        return 'Message<Type={}, To={}>'.format(self._type, self._to)

    def copy(self):
        return Message.recv(data=self.toDict())

    def set_reject(self, reject, maintain_data=False):
        if maintain_data:
            self._data['reject'] = reject
        else:
            self._data = {
                'reject': reject
            }

    def is_reject(self):
        return 'reject' in self._data

    def is_broadcast(self):
        return self._to[0] == 'broadcast'

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
        if type(data) is not dict:
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

    def __init__(self, pkt_type, peer, can_broadcast=False):
        self.pkt_type = pkt_type
        self.peer = peer
        self.can_broadcast = can_broadcast

    # Wrap if it is a broadcast packet.
    def wrap_packet(self, message, **kwargs):
        arr = []
        if self.can_broadcast and message.is_broadcast():
            role = message._to[1]
            for each in self.peer.connectlist:
                if role == 'all' or each.role == role:
                    message._to = each.host
                    arr.append(message.copy())
        else:
            arr.append(message)
        return arr

    def onSend(self, target, **kwargs):
        if 'reject_reason' in locals()['kwargs']:
            message = self.onSendReject(target=target, **kwargs)
            return message if type(message) is list else [message]
        else:
            message = self.onSendPkt(target=target, **kwargs)
            return self.wrap_packet(message=message, **kwargs)

    def onSendReject(self, target, reject_reason, **kwargs):
        message = Message(_to=target, _from=self.peer.peer_info.host,
                          _hash=None, _type=self.pkt_type, _data={})
        message.set_reject(reject_reason)
        return message

    def onSendPkt(self, target, **kwargs):
        raise NotImplementedError

    def onRecv(self, src, data, **kwargs):
        if 'reject' in data:
            self.onRecvReject(src=src, data=data, **kwargs)
        else:
            self.onRecvPkt(src=src, data=data, **kwargs)

    def onRecvReject(self, src, data, **kwargs):
        reject = data['reject']
        printText('Rejected by {}, reason: {}'.format(src, reject))

    def onRecvPkt(self, src, data, **kwargs):
        raise NotImplementedError
