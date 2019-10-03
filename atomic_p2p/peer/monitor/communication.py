import time

from atomic_p2p.communication import Packet, Handler
from atomic_p2p.peer.entity.peer_status import StatusType


class CheckHandler(Handler):
    pkt_type = "monitor-check"

    def __init__(self, monitor):
        super().__init__(pkt_type=type(self).pkt_type, peer=monitor.peer)
        self.monitor = monitor

    def _build_accept_packet(self, target):
        self.monitor.peer_status_update_by_host(host=target)
        data = {"send_ts": time.time()}
        return Packet(
            dst=target,
            src=self.peer.server_info.host,
            program_hash=self.peer.program_hash,
            _type=self.pkt_type,
            _data=data,
        )

    def on_recv_pkt(self, src, pkt, conn):
        data = pkt.data
        message = "WatchDog check from {}: send ts {}".format(pkt.src, data["send_ts"])
        if self.monitor.verbose:
            self.monitor.logger.warning(message)

    def on_recv_reject_pkt(self, src, pkt, conn):
        if self.monitor.verbose:
            super().on_recv_reject_pkt(src, pkt, conn)
        self.monitor.peer_status_update_by_host(host=pkt.src)
