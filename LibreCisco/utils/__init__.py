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
