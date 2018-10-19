from LibreCisco.utils import checkNet


def test_checkNet():
    assert checkNet('this is not a url') is False
    assert checkNet() is True
