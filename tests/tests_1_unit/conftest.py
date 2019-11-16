import os
from os import getcwd
from os.path import join
import time
import pytest

from atomic_p2p.utils import self_hash as sh, create_self_signed_cert, DNSResolver
from atomic_p2p.peer import ThreadPeer


@pytest.fixture(scope="session")
def dns_resolver():
    return DNSResolver(ns="127.0.0.1", role="switch")


@pytest.fixture(scope="session")
def self_hash():
    return sh(join(os.getcwd(), "atomic_p2p"))


@pytest.fixture(scope="session")
def cert():
    return create_self_signed_cert(getcwd(), "data/test.pem", "data/test.key")


@pytest.yield_fixture(scope="module")
def default_peer(cert, self_hash):
    p = ThreadPeer(host=("0.0.0.0", 8000), name="name", role="role",
                    cert=cert, program_hash=self_hash, auto_register=True)
    p.start()

    yield p
    time.sleep(1)
    p.stop()


@pytest.yield_fixture(scope="module")
def default_peer2(cert, self_hash):
    p = ThreadPeer(host=("0.0.0.0", 8001), name="name2", role="role",
                    cert=cert, program_hash=self_hash, auto_register=True)
    p.start()
    yield p
    time.sleep(1)
    p.stop()
