import os
from os import getcwd
from os.path import join
import time
import pytest

from atomic_p2p.peer import Peer
from atomic_p2p.peer.communication.net import JoinHandler
from atomic_p2p.utils.security import self_hash as sh, create_self_signed_cert


@pytest.fixture(scope="session")
def self_hash():
    return sh(join(os.getcwd(), "atomic_p2p"))


@pytest.fixture(scope="session")
def cert():
    return create_self_signed_cert(getcwd(), "data/test.pem", "data/test.key")


@pytest.yield_fixture(scope="function")
def malware_peer(cert):
    malware_hash = sh(join(getcwd(), "atomic_p2p", "peer"))
    mp = Peer(role="sw", name="switch_malware", host=("127.0.0.1", 8012),
              cert=cert, _hash=malware_hash)
    mp.start()
    yield mp
    mp.stop()
    time.sleep(1)


@pytest.yield_fixture(scope="function")
def core1(cert, self_hash):
    core = Peer(role="core", name="core01",
                host=("127.0.0.1", 8000), cert=cert, _hash=self_hash)
    core.start()
    yield core
    core.stop()
    time.sleep(1)


@pytest.yield_fixture(scope="function")
def switch1(cert, self_hash):
    switch = Peer(role="sw", name="switch01",
                  host=("127.0.0.1", 8010), cert=cert, _hash=self_hash)
    switch.start()
    yield switch
    switch.stop()
    time.sleep(1)


@pytest.yield_fixture(scope="function")
def switch2(cert, self_hash):
    switch = Peer(role="sw", name="switch02",
                  host=("127.0.0.1", 8011), cert=cert, _hash=self_hash)
    switch.start()
    yield switch
    switch.stop()
    time.sleep(1)


@pytest.yield_fixture(scope="session")
def net(cert, self_hash):
    nodes = {
        "core_1": Peer(role="core", name="core01",
                  host=("127.0.0.1", 8000), cert=cert, _hash=self_hash),
        "switch_1": Peer(role="sw", name="switch01",
                  host=("127.0.0.1", 8010), cert=cert, _hash=self_hash),
        "switch_2": Peer(role="sw", name="switch02",
                  host=("127.0.0.1", 8011), cert=cert, _hash=self_hash)
    }

    for (_, val) in nodes.items():
        val.start()

    nodes["switch_1"].onProcess(["join", "127.0.0.1:8000"])
    nodes["switch_2"].onProcess(["join", "127.0.0.1:8000"])

    time.sleep(8)
    yield nodes
    for (_, val) in nodes.items():
        val.stop()