from json import loads

from atomic_p2p.communication import Packet


def test_init(packet, default_peer, self_hash):
    assert packet.dst == ("0.0.0.0", 9000)
    assert packet._type == "a"
    assert packet.data == {"test": "test text"}

    assert Packet(
        dst=("0.0.0.0", 9000),
        src=default_peer.server_info.host,
        program_hash=self_hash,
        _type="str",
        _data={},
    ).dst == ("0.0.0.0", 9000)


def test_str(packet):
    assert str(packet) == "Packet<DST={} SRC={} TYP={}>".format(
        packet.dst, packet.src, packet._type
    )


def test_set_reject(packet):
    assert "reject" not in packet.data
    assert packet.data == {"test": "test text"}
    packet.set_reject("456", maintain_data=True)
    assert packet.data == {"test": "test text", "reject": "456"}
    packet.set_reject("123")
    assert packet.data == {"reject": "123"}


def test_is_reject(packet):
    assert packet.is_reject() is False
    packet.set_reject("123")
    assert packet.is_reject() is True


def test_to_dict(packet, default_peer):
    assert packet.to_dict() == {
        "to": {"ip": packet.dst[0], "port": int(packet.dst[1])},
        "from": {
            "ip": default_peer.server_info.host[0],
            "port": int(default_peer.server_info.host[1]),
        },
        "hash": packet.program_hash,
        "type": packet._type,
        "data": packet.data,
    }


def test_serilize(packet):
    send_data = str(Packet.serilize(packet), encoding="utf-8")
    data = loads(send_data)
    assert data["to"]["ip"] == packet.dst[0]
    assert data["to"]["port"] == int(packet.dst[1])
    assert data["type"] == packet._type
    assert data["data"] == packet.data


def test_deserilize(packet):
    dict_data = packet.serilize(packet)
    data = Packet.deserilize(dict_data)
    assert data.dst == ("0.0.0.0", 9000)
    assert data._type == "a"
    assert data.data == {"test": "test text"}
