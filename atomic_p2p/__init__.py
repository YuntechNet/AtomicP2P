from os import getcwd
from os.path import join

from atomic_p2p.logging import getLogger
from atomic_p2p.peer import ThreadPeer
from atomic_p2p.utils import create_self_signed_cert as cssc, self_hash


__version__ = "0.0.5"


class AtomicP2P(object):

    # TODO: Arguments need redefine, cause the format is not very clear enough.
    #       Also, whole class should add type hint.
    #                   2019/05/13
    def __init__(
        self, role: str, addr: str, name: str, cert: str, logger: "logging.Logger"
    ) -> None:
        """Init of AtomicP2P object
        Args:
            role: str represents peer's role.
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

        hash_str = self_hash(path=join(getcwd(), "atomic_p2p"))
        addr = addr.split(":") if type(addr) is str else addr

        self.services = {
            "peer": ThreadPeer(
                host=addr,
                name=name,
                role=role,
                program_hash=hash_str,
                ns=None,
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
