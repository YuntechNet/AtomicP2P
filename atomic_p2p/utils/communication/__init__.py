from typing import Tuple
from ssl import get_server_certificate
from socket import (
    inet_pton, inet_aton, AF_INET, AF_INET6, error, socket, SOCK_STREAM
)

from atomic_p2p.utils import host_valid
from atomic_p2p.utils.communication.packet import Packet
from atomic_p2p.utils.communication.handler import Handler


def valid_ipv4_format(address: str) -> bool:
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


def valid_ipv6_format(address: str) -> bool:
    try:
        inet_pton(AF_INET6, address)
    except error:  # not a valid address
        return False
    return True


def is_ssl_socket_open(host: Tuple[str, int]) -> bool:
    assert host_valid(host) is True
    try:
        get_server_certificate(host)
        return True
    except Exception:
        return False
