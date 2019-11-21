from os import getcwd
from os.path import join
from time import sleep
from pytest import fixture, yield_fixture

from atomic_p2p.utils import DNSResolver, self_hash as sh, create_self_signed_cert
from atomic_p2p.peer import ThreadPeer
from atomic_p2p.peer.entity import PeerRole


@fixture(scope="module")
def dns_resolver():
    return DNSResolver(ns="127.0.0.1")


@fixture(scope="session")
def self_hash():
    return sh(join(getcwd(), "atomic_p2p"))


@fixture(scope="session")
def cert():
    return create_self_signed_cert(getcwd(), "data/test.pem", "data/test.key")


@yield_fixture(scope="module")
def default_peer(dns_resolver, cert, self_hash):
    p = ThreadPeer(
        dns_resolver=dns_resolver,
        host=("0.0.0.0", 8000),
        name="name",
        role=PeerRole.CORE,
        cert=cert,
        program_hash=self_hash,
        auto_register=True,
    )
    p.start()

    yield p
    sleep(1)
    p.stop()


@yield_fixture(scope="module")
def default_peer2(dns_resolver, cert, self_hash):
    p = ThreadPeer(
        dns_resolver=dns_resolver,
        host=("0.0.0.0", 8001),
        name="name2",
        role=PeerRole.CORE,
        cert=cert,
        program_hash=self_hash,
        auto_register=True,
    )
    p.start()
    yield p
    sleep(1)
    p.stop()
