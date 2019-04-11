from dns.reversename import from_address
from dns.resolver import Resolver, query

from LibreCisco.peer.peer_info import PeerInfo
from LibreCisco.utils.manager import ThreadManager


class PoolMaintainer(ThreadManager):
    """A object responsible for keep updating peer info pool from DNS
    This object will maintain every records in DNS such as global and self-ser-
    vice pool.
    """

    def __init__(self, ns, role, domain, loopDelay=300):
        """Init of PoolMaintainer
        Args:
            ns: A string or list which contains all avaiable nameservers.
            role: A string represent current peer's service type.
            domain: A string represent whole nets domain.
            loopDelay: A integer controlls update period, default is 300 secs.
        """
        super(PoolMaintainer, self).__init__(loopDelay=loopDelay)
        self._ns = ns if type(ns) is list else [ns]
        self._role = role
        self._domain = domain
        self._resolver = Resolver(configure=False)
        self._resolver.nameservers = self._ns

        self._globalPeerPool = []
        self._servicePeerPool = []

    def run(self):
        while not self.stopped.wait(self.loopDelay):
            self.syncFromDNS()

    def syncFromDNS(self):
        """Query from DNS fetch all records and put in pool
        Hard-code with global.[domain] will send to DNS for query. Durring pro-
        cessing each record, if any error occured, then it will be skip.
        The fianl result would be all DNS record been parse to PeerInfo and put
        at each peer pool in class variable.
        """
        records = self.forward('global.' + self._domain)
        for each in records:
            name, role, fqdn, addr = self.fqdnInfo(each)
            priority, weight, port, srv_fqdn = self.srv(fqdn)
            if name is not None and srv_fqdn is not None:
                peer_info = PeerInfo(name=name, role=role,
                                     host=(addr, int(port)))
                if role == self._role and \
                   peer_info not in self._servicePeerPool:
                    self._servicePeerPool.append(peer_info)
                elif peer_info not in self._globalPeerPool:
                    self._globalPeerPool.append(peer_info)

    def fqdnInfo(self, addr):
        """Get a address's fqdn and split it
        Args:
            addr: A IPv4 format string.
        Returns:
            Toupe contains name, role, fqdn and original address.
            Each element would be string.
            Any error cause failure will turn elements to None.
        """
        fqdn = self.reverse(addr)[0][:-1]
        if fqdn != []:
            splits = fqdn.split('.')
            return splits[0], splits[1], fqdn, addr
        else:
            return None, None, None, None

    def forward(self, fqdn):
        try:
            answers = self._resolver.query(fqdn, 'A')
            return [str(x) for x in answers]
        except Exception:
            return []

    def reverse(self, address):
        try:
            answers = self._resolver.query(from_address(address), 'PTR')
            return [str(x) for x in answers]
        except Exception:
            return []

    def srv(self, fqdn):
        try:
            return str(self._resolver.query(
                '_yunnms._tcp.' + fqdn, 'SRV')[0]).split(' ')
        except Exception:
            return 0, 0, -1, None
