from typing import Tuple
from time import sleep
from multiprocessing import Process, Event

from atomic_p2p.peer import Peer
from atomic_p2p.peer.communication import DisconnectHandler
from atomic_p2p.utils.logging import getLogger


class ProcessPeer(Peer, Process):
    def __init__(
        self,
        host: Tuple[str, int],
        name: str,
        role: str,
        cert: Tuple[str, str],
        program_hash: str,
        ns: str = None,
        loop_delay: int = 1,
        auto_register: bool = False,
        logger: "logging.Logger" = getLogger(__name__),
    ):
        super().__init__(
            host=host,
            name=name,
            role=role,
            cert=cert,
            program_hash=program_hash,
            ns=ns,
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
