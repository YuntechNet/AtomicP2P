import json
from LibreCisco.utils.communication import Packet


def test_init(message, default_peer, self_hash):
    assert message._to == ('0.0.0.0', 9000)
    assert message._type == 'a'
    assert message._data == {'test': 'test text'}

    assert Packet(dst=('0.0.0.0', 9000), src=default_peer.peer_info.host,
                  _hash=self_hash, _type='str',
                  _data={})._to == ('0.0.0.0', 9000)


def test_str(message):
    assert str(message) == 'Packet<DST={} SRC={} TYP={}>'.format(
                message._to, message._from, message._type)


def test_set_reject(message):
    assert 'reject' not in message._data
    assert message._data == {'test': 'test text'}
    message.set_reject('456', maintain_data=True)
    assert message._data == {
        'test': 'test text',
        'reject': '456'
    }
    message.set_reject('123')
    assert message._data == {'reject': '123'}


def test_is_reject(message):
    assert message.is_reject() is False
    message.set_reject('123')
    assert message.is_reject() is True


def test_toDict(message, default_peer):
    assert message.toDict() == {
        'to': {
            'ip': message._to[0],
            'port': int(message._to[1])
        },
        'from': {
            'ip': default_peer.peer_info.host[0],
            'port': int(default_peer.peer_info.host[1])
        },
        'hash': message._hash,
        'type': message._type,
        'data': message._data
    }


def test_send(message):
    send_data = str(Packet.send(message), encoding='utf-8')
    data = json.loads(send_data)
    assert data['to']['ip'] == message._to[0]
    assert data['to']['port'] == int(message._to[1])
    assert data['type'] == message._type
    assert data['data'] == message._data


def test_recv(message):
    dict_data = message.send(message)
    data = Packet.recv(dict_data)
    assert data._to == ('0.0.0.0', 9000)
    assert data._type == 'a'
    assert data._data == {'test' :'test text'}
