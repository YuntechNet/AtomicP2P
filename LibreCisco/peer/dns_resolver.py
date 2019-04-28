from typing import Union, Dict, List, Tuple
from dns.reversename import from_address
from dns.resolver import Resolver, query

from LibreCisco.peer.entity.peer_info import PeerInfo
from LibreCisco.utils.manager import ThreadManager


class DNSResolver(object):
    """A object responsible for keep updating peer info pool from DNS
    This object will maintain every records in DNS such as global and self-ser-
    vice pool.
    """

    def __init__(self, ns: Union[str, List[str]], role: str) -> None:
        """Init of DNSResolver

        Args:
            ns: All avaiable nameservers.
            role: Current peer's service type.
            loopDelay: Update period, default is 300 secs.
        """
        self._ns = ns if type(ns) is list else [ns]
        self._role = role
        self._resolver = Resolver(configure=False)
        self._resolver.nameservers = self._ns

    def change_ns(self, ns:List[str]) -> None:
        assert type(ns) is list
        self._ns = ns
        self._resolver.nameserver = self._ns

    def sync_from_DNS(self, current_host: Tuple[str, int],
                      domain: str) -> List['PeerInfo']:
        """Query from DNS fetch all records and put in pool
        Hard-code with global.[domain] will send to DNS for query. Durring pro-
        cessing each record, if any error occured, then it will be skip.
        The fianl result would be all DNS record been parse to PeerInfo and put
        at each peer pool in class variable.

        Args:
            domain: Whole net's domain.

        Returns:
            Query results in list with PeerInfo from DNS.
        """
        peers = []
        records = self.forward('global.' + domain)
        for each in records:
            name, role, fqdn, addr = self.get_fqdn_info(each)
            # TODO: Seeking better solution determine whether get_fqdn_info()
            #       is valid or not, Currently each call will produce N+1 
            #       querys to DNS.
            _, _, port, srv_fqdn = tuple(self.srv(fqdn))
            if name is not None and srv_fqdn is not None:
                peer_info = PeerInfo(name=name, role=role,
                                     host=(addr, int(port)))
                if peer_info not in peers and peer_info.host != current_host:
                    peers.append(peer_info)
        return peers

    def get_fqdn_info(self, addr: str) -> Tuple[str, str, str, str]:
        """Get a address's fqdn and split it

        Args:
            addr: A IPv4 format string.

        Returns:
            Toupe contains name, role, fqdn and original address.
            Each element would be string.
            Any error cause failure will turn elements to None.
        """
        try:
            fqdn = self.reverse(addr)[0][:-1]
            splits = fqdn.split('.')
            return splits[0], splits[1], fqdn, addr
        except Exception:
            return None, None, None, None

    def forward(self, fqdn: str) -> List:
        try:
            answers = self._resolver.query(fqdn, 'A')
            return [str(x) for x in answers]
        except Exception:
            return []

    def reverse(self, address: str) -> List:
        try:
            answers = self._resolver.query(from_address(address), 'PTR')
            return [str(x) for x in answers]
        except Exception:
            return []

    def srv(self, fqdn: str) -> List:
        try:
            return str(self._resolver.query(
                '_yunnms._tcp.' + fqdn, 'SRV')[0]).split(' ')
        except Exception:
            return [0, 0, -1, None]
