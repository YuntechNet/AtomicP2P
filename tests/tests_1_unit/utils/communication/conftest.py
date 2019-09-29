from pytest import fixture

from atomic_p2p.communication import Packet, Handler


@fixture(scope="class")
def packet(default_peer, self_hash):
    return Packet(dst=("0.0.0.0", 9000), src=default_peer.server_info.host,
                  program_hash=self_hash, _type="a", _data={"test": "test text"})


@fixture(scope="class")
def handler(default_peer):
    return Handler(peer=default_peer, pkt_type="test_key")
