import json
from utils.message import Message

def test_init(message):
    assert message._host == ('0.0.0.0', 9000)
    assert message._type == 'a'
    assert message._data == 'test text'

    assert Message(_host=('0.0.0.0', '9000'), _type=None, _data=None)._host == ('0.0.0.0', 9000)

def test_str(message):
    assert str(message) == 'Message<>'

def test_toDict(message):
    assert message.toDict() == {
        'host': {
            'ip': message._host[0],
            'port': int(message._host[1])
        },
        'type': message._type,
        'data': message._data
    }

def test_send(message):
    send_data = str(Message.send(message), encoding='utf-8')
    data = json.loads(send_data)
    assert data['host']['ip'] == message._host[0]
    assert data['host']['port'] == int(message._host[1])
    assert data['type'] == message._type
    assert data['data'] == message._data

def test_recv(message):
    dict_data = message.send(message)
    data = Message.recv(dict_data)
    assert data._host == ('0.0.0.0', 9000)
    assert data._type == 'a'
    assert data._data == 'test text'

        
