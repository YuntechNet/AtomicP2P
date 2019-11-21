from os import getcwd
from os.path import join
from time import sleep
from pytest import fixture, yield_fixture

from atomic_p2p.peer import ThreadPeer
from atomic_p2p.peer.entity import PeerRole
from atomic_p2p.utils import DNSResolver, self_hash as sh, create_self_signed_cert


@fixture(scope="module")
def dns_resolver():
    return DNSResolver(ns="127.0.0.1")


@fixture(scope="session")
def self_hash():
    return sh(join(getcwd(), "atomic_p2p"))


@fixture(scope="session")
def cert():
    return create_self_signed_cert(getcwd(), "data/test.pem", "data/test.key")


@yield_fixture(scope="function")
def malware_peer(dns_resolver, cert):
    malware_hash = sh(join(getcwd(), "atomic_p2p", "peer"))
    mp = ThreadPeer(
        dns_resolver=dns_resolver, role=PeerRole.EDGE, name="edge_malware",
        host=("127.0.0.1", 8012), cert=cert, program_hash=malware_hash,
        auto_register=True)
    mp.start()
    yield mp
    mp.stop()
    sleep(3)


@yield_fixture(scope="function")
def core1(dns_resolver, cert, self_hash):
    core = ThreadPeer(
        dns_resolver=dns_resolver, role=PeerRole.CORE, name="core01",
        host=("127.0.0.1", 8000), cert=cert, program_hash=self_hash,
        auto_register=True)
    core.start()
    yield core
    core.stop()
    sleep(3)


@yield_fixture(scope="function")
def edge1(dns_resolver, cert, self_hash):
    edge = ThreadPeer(
        dns_resolver=dns_resolver, role=PeerRole.EDGE, name="edge01",
        host=("127.0.0.1", 8010), cert=cert, program_hash=self_hash,
        auto_register=True)
    edge.start()
    yield edge
    edge.stop()
    sleep(3)


@yield_fixture(scope="function")
def edge2(dns_resolver, cert, self_hash):
    edge = ThreadPeer(
        dns_resolver=dns_resolver, role=PeerRole.EDGE, name="edge02",
        host=("127.0.0.1", 8011), cert=cert, program_hash=self_hash,
        auto_register=True)
    edge.start()
    yield edge
    edge.stop()
    sleep(3)


@yield_fixture(scope="session")
def net(dns_resolver, cert, self_hash):
    nodes = {
        "core_1": ThreadPeer(
            dns_resolver=dns_resolver, role=PeerRole.CORE, name="core01",
            host=("127.0.0.1", 8000), cert=cert, program_hash=self_hash,
            auto_register=True),
        "edge_1": ThreadPeer(
            dns_resolver=dns_resolver, role=PeerRole.EDGE, name="edge01",
            host=("127.0.0.1", 8010), cert=cert, program_hash=self_hash,
            auto_register=True),
        "edge_2": ThreadPeer(
            dns_resolver=dns_resolver, role=PeerRole.EDGE, name="edge02",
            host=("127.0.0.1", 8011), cert=cert, program_hash=self_hash,
            auto_register=True)
    }

    for (_, val) in nodes.items():
        val.start()

    nodes["edge_1"].join_net(host=("127.0.0.1", 8000))
    nodes["edge_2"].join_net(host=("127.0.0.1", 8000))

    sleep(12)
    yield nodes
    for (_, val) in nodes.items():
        val.stop()
    sleep(12)
