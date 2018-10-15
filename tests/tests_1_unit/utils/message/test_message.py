import json
from LibreCisco.utils.message import Message

def test_init(message, default_peer, self_hash):
    assert message._to == ('0.0.0.0', 9000)
    assert message._type == 'a'
    assert message._data == 'test text'

    assert Message(_to=('0.0.0.0', '9000'), _from=default_peer.host, _hash=self_hash, _type=None, _data=None)._to == ('0.0.0.0', 9000)

def test_str(message):
    assert str(message) == 'Message<>'

def test_set_reject(message):
    assert not 'reject' in message._data
    message.set_reject('123')
    assert message._data == {'reject': '123'}
    message._data = {
        'test': 'exists'
    }
    message.set_reject('456', maintain_data=True)
    assert message._data == {
        'test': 'exists',
        'reject': '456'
    }

def test_is_reject(message):
    assert message.is_reject() == False
    message.set_reject('123')
    assert message.is_reject() == True

def test_toDict(message, default_peer):
    assert message.toDict() == {
        'to': {
            'ip': message._to[0],
            'port': int(message._to[1])
        },
        'from': {
            'ip': default_peer.host[0],
            'port': int(default_peer.host[1])
        },
        'hash': message._hash,
        'type': message._type,
        'data': message._data
    }

def test_send(message):
    send_data = str(Message.send(message), encoding='utf-8')
    data = json.loads(send_data)
    assert data['to']['ip'] == message._to[0]
    assert data['to']['port'] == int(message._to[1])
    assert data['type'] == message._type
    assert data['data'] == message._data

def test_recv(message):
    dict_data = message.send(message)
    data = Message.recv(dict_data)
    assert data._to == ('0.0.0.0', 9000)
    assert data._type == 'a'
    assert data._data == 'test text'

        
