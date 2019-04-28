from LibreCisco.utils.communication.packet import Packet
from LibreCisco.utils.communication.handler import Handler

from socket import inet_pton, inet_aton, AF_INET, AF_INET6, error

def valid_ipv4_format(address):
    try:
        inet_pton(AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            inet_aton(address)
        except error:
            return False
        return address.count('.') == 3
    except error:  # not a valid address
        return False

    return True

def valid_ipv6_format(address):
    try:
        inet_pton(AF_INET6, address)
    except error:  # not a valid address
        return False
    return True

