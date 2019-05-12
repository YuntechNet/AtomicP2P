import sys
import urllib
import urllib.request


def checkNet(url='https://www.google.com.tw'):
    try:
        urllib.request.urlopen(url)
        return True
    except Exception as e:
        pass
    return False


def getExternalIP():
    try:
        return urllib.request.urlopen('http://ip.42.pl/raw').read()
    except Exception as e:
        return None


def host_valid(host):
    assert type(host) == tuple
    assert len(host) == 2
    assert type(host[0]) == str
    assert type(host[1]) == int
    assert host[1] > 0 and host[1] < 65535
    return True
