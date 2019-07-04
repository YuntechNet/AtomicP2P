from atomic_p2p.utils import checkNet


def test_checkNet():
    assert checkNet("this is not a url") is False
    rtn = checkNet()
    if rtn is False:
        assert checkNet(url="http://www.speedtest.net")
    else:
        assert rtn is True
