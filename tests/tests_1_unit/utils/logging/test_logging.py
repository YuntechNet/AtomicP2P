from logging import getLogger as nativeGetLogger

from atomic_p2p.logging import getLogger


def test_getLogger():
    assert getLogger() == nativeGetLogger()
    logger = getLogger("test")
    assert logger == nativeGetLogger("test")
