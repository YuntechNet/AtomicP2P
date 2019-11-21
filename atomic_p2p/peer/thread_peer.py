from typing import Tuple, List
from time import sleep
from threading import Thread, Event

from ..logging import getLogger
from .peer import Peer
from .entity import PeerRole


class ThreadPeer(Peer, Thread):
    def __init__(
        self,
        dns_resolver: "DNSResolver",
        host: Tuple[str, int],
        name: str,
        role: "enum.Enum",
        cert: Tuple[str, str],
        program_hash: str,
        bind_address: str = "0.0.0.0",
        peer_role_type: "enum.EnumMeta" = PeerRole,
        loop_delay: int = 1,
        auto_register: bool = False,
        logger: "logging.Logger" = getLogger(__name__),
    ):
        super().__init__(
            dns_resolver=dns_resolver,
            host=host,
            name=name,
            role=role,
            cert=cert,
            program_hash=program_hash,
            peer_role_type=peer_role_type,
            bind_address=bind_address,
            auto_register=auto_register,
            logger=logger,
        )
        self.loopDelay = loop_delay
        self.stopped = Event()
        self.started = Event()

    def is_start(self) -> bool:
        return self.started.is_set()

    def start(self) -> None:
        super().start()
        self.loop_start()
        self.started.set()

    def stop(self) -> None:
        self.loop_stop()
        self.stopped.set()
        self.started.clear()

    def run(self) -> None:
        while self.stopped.wait(self.loopDelay) is False or self.send_queue != {}:
            self.loop()
        self.loop_stop_post()
        sleep(2)
        self.logger.info("{} stopped.".format(self.server_info))
