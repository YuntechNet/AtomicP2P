from typing import Union, List, Tuple
from dns.reversename import from_address
from dns.resolver import Resolver, query

from LibreCisco.peer.entity.peer_info import PeerInfo
from LibreCisco.utils.manager import ThreadManager


class PoolMaintainer(ThreadManager):
    """A object responsible for keep updating peer info pool from DNS
    This object will maintain every records in DNS such as global and self-ser-
    vice pool.
    """

    def __init__(self, ns: Union[str, List[str]], role: str, domain: str,
                 loopDelay: int = 300) -> None:
        """Init of PoolMaintainer

        Args:
            ns: All avaiable nameservers.
            role: Current peer's service type.
            domain: Whole net's domain.
            loopDelay: Update period, default is 300 secs.
        """
        super(PoolMaintainer, self).__init__(loopDelay=loopDelay)
        self._ns = ns if type(ns) is list else [ns]
        self._role = role
        self._domain = domain
        self._resolver = Resolver(configure=False)
        self._resolver.nameservers = self._ns

        self._globalPeerPool = []
        self._servicePeerPool = []

    def run(self) -> None:
        while not self.stopped.wait(self.loopDelay):
            self.syncFromDNS()

    def syncFromDNS(self) -> None:
        """Query from DNS fetch all records and put in pool
        Hard-code with global.[domain] will send to DNS for query. Durring pro-
        cessing each record, if any error occured, then it will be skip.
        The fianl result would be all DNS record been parse to PeerInfo and put
        at each peer pool in class variable.
        """
        records = self.forward('global.' + self._domain)
        for each in records:
            name, role, fqdn, addr = self.fqdnInfo(each)
            # TODO: Seeking better solution at determine whether fqdnInfo() is
            #       valid or not, Currently each call will produce N+1 querys
            #       to DNS.
            priority, weight, port, srv_fqdn = tuple(self.srv(fqdn))
            if name is not None and srv_fqdn is not None:
                peer_info = PeerInfo(name=name, role=role,
                                     host=(addr, int(port)))
                # TODO: sevicePeerPool should be a duplicate contents of
                #       PeerInfo insides globalPeerPool.
                if role == self._role and \
                   peer_info not in self._servicePeerPool:
                    self._servicePeerPool.append(peer_info)
                elif peer_info not in self._globalPeerPool:
                    self._globalPeerPool.append(peer_info)

    def fqdnInfo(self, addr: str) -> Tuple[str, str, str, str]:
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
