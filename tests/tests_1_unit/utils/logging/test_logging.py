import logging

from atomic_p2p.logging import getLogger


def test_getLogger():
    assert getLogger() == logging.getLogger()
    logger = getLogger("test")
    assert logger == logging.getLogger("test")
