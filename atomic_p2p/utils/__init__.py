from .security import create_self_signed_cert, self_hash

__all__ = ["create_self_signed_cert", "self_hash", "host_valid"]


def host_valid(host):
    assert type(host) == tuple
    assert len(host) == 2
    assert type(host[0]) == str
    assert type(host[1]) == int
    assert host[1] > 0 and host[1] < 65535
    return True
