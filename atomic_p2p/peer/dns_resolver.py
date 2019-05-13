from typing import Union, Dict, List, Tuple
from dns.reversename import from_address
from dns.resolver import Resolver, query

from atomic_p2p.peer.entity.peer_info import PeerInfo
from atomic_p2p.utils.manager import ThreadManager


class DNSResolver(object):
    """A object responsible for keep updating peer info pool from DNS
    This object will maintain every records in DNS such as global and self-
    service pool.
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

    def change_ns(self, ns: List[str]) -> None:
        """Change resolver's namserver host.

        Args:
            ns: nameservers to change to.
        """
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
            for every in self.reverse(address=each):
                split = every.split('.')
                name, role, fqdn, addr = split[0], split[1], every, each
                if name is None or 'localhost' in name:
                    continue
                # TODO: Seeking better solution determine whether
                #       get_fqdn_info() is valid or not, Currently each call
                #       will produce N+1 querys to DNS.
                _, _, port, srv_fqdn = self.srv(fqdn=fqdn)
                if name is not None and srv_fqdn is not None:
                    peer_info = PeerInfo(
                        name=name, role=role, host=(addr, int(port)))
                    if (peer_info not in peers and
                            peer_info.host != current_host):
                        peers.append(peer_info)
        return peers

    def forward(self, fqdn: str) -> List[str]:
        """Wraped function to query A records.

        Args:
            fqdn: fqdn to be query.

        Returns:
            A records of given fqdn in list with str.
            Exceptions occurr will return a empty list.
        """
        try:
            answers = self._resolver.query(fqdn, 'A')
            return [str(x) for x in answers]
        except Exception:
            return []

    def reverse(self, address: str) -> List[str]:
        """Wrapped function to query PTR records.

        Args:
            address: address to be query.

        Returns:
            PTR records of give address in list with str.
            Exceptions occurr will return a empty list
        """
        try:
            answers = self._resolver.query(from_address(address), 'PTR')
            return [str(x) for x in answers]
        except Exception:
            return []

    def srv(self, fqdn: str) -> Tuple[int, int, int, str]:
        """Wrapped function to query SRV records.

        Args:
            fqdn: fqdn to be query.

        Returns:
            Give a tuple with four varialbe with:
            priority, weight, port, and srv_fqdn
            Exceptions occurr will return with (0, 0, -1, None)
        """
        try:
            res = str(self._resolver.query(
                '_atomic_p2p._tcp.' + fqdn, 'SRV')[0]).split(' ')
            return (res[0], res[1], res[2], res[3])
        except Exception as e:
            return (0, 0, -1, None)
