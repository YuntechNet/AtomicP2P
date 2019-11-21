from typing import Tuple
from os import getcwd
from os.path import join

from .logging import getLogger
from .peer import ThreadPeer
from .utils import create_self_signed_cert as cssc, self_hash


__version__ = "0.0.6"


class AtomicP2P(object):

    # TODO: Arguments need redefine, cause the format is not very clear enough.
    #       Also, whole class should add type hint.
    #                   2019/05/13
    def __init__(
        self,
        dns_resolver: "DNSResolver",
        bind_address: str,
        role: "enum.Enum",
        host: Tuple[str, int],
        name: str,
        cert: str,
        logger: "logging.Logger",
    ) -> None:
        """Init of AtomicP2P object
        Args:
            role: Enum represents peer's role.
            addr: str with `ip:port` format, peer server will listen on.
            name: str represents peer's name.
            cert: str represents cert file's path, should directly point to
                cert file. like `data/atomic_p2p.pem`, and key file should
                same as cert file exception sub-extension with `.key`.
        """
        cert_file, key_file = cssc(
            cert_dir=getcwd(), cert_file=cert, key_file=cert.replace(".pem", ".key")
        )
        self.logger = logger
        self.services = {
            "peer": ThreadPeer(
                dns_resolver=dns_resolver,
                bind_address=bind_address,
                host=host,
                name=name,
                role=role,
                program_hash=self_hash(path=join(getcwd(), "atomic_p2p")),
                cert=(cert_file, key_file),
                auto_register=True,
                logger=self.logger,
            )
        }
        self.services["monitor"] = self.services["peer"].monitor

    def start(self):
        for each in self.services:
            if self.services[each].is_start() is False:
                self.services[each].start()
        self.logger.info("Platform started.")

    def stop(self):
        for each in self.services:
            self.services[each].stop()

    def _on_command(self, cmd):
        if type(cmd) != list and type(cmd) == str:
            cmd = cmd.split(" ")

        service_key = cmd[0].lower()
        if service_key in self.services:
            return (True, self.services[service_key]._on_command(cmd[1:]))
        elif service_key == "monitor":
            return (True, self.services["peer"]._on_command(cmd[1:]))
        elif service_key == "stop":
            self.stop()
            return (True, None)
        else:
            help_tips = (
                "peer help            - See peer's help\n"
                "monitor help        - See monitor's help\n"
                "exit/stop            - exit the whole program.\n"
            )
            return (True, help_tips)
