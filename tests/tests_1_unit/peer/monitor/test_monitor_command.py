def test_helpCmd(default_peer):
    assert default_peer.monitor._on_command(["help"]) == (
        "monitor [cmd] <options>\n"
        " - pause                                          "
        "pause monitor's main loop thread.\n"
        " - period [seconds]                               "
        "change monitor's loop period to another second.\n"
        " - list                                           "
        "list each statuses in list.\n"
        " - reset [peer name/role/all]                     "
        "reset all or specific name or role's peer status t"
        "o PENDING."
    )
    assert "PauseCmd" in default_peer.monitor._on_command(["help", "pause"])


def test_pauseCmd(default_peer):
    assert default_peer.monitor.pause is False
    default_peer.monitor._on_command(["pause"])
    assert default_peer.monitor.pause is True
    default_peer.monitor._on_command(["pause"])
    assert default_peer.monitor.pause is False


def test_periodCmd(default_peer):
    origin = default_peer.monitor.loopDelay
    default_peer.monitor._on_command(["period", "a"])
    assert default_peer.monitor.loopDelay == origin
    default_peer.monitor._on_command(["period", "111"])
    assert default_peer.monitor.loopDelay == 111
    default_peer.monitor._on_command(["period", str(origin)])


def test_verboseCmd(default_peer):
    assert default_peer.monitor.verbose is False
    default_peer.monitor._on_command(["verbose"])
    assert default_peer.monitor.verbose is True
    default_peer.monitor._on_command(["verbose"])
    assert default_peer.monitor.verbose is False
