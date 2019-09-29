

def test_init(thread):
    assert thread.loopDelay == 1
    assert thread.stopped.is_set() is False


def test_start(thread):
    thread.start()


def test_stop(thread):
    thread.stop()
    assert thread.stopped.is_set()
