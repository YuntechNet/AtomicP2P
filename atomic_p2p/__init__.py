from os import getcwd
from os.path import join

from atomic_p2p.peer import Peer
from atomic_p2p.local_monitor import LocalMonitor
from atomic_p2p.utils.security import (
    create_self_signed_cert as cssc, self_hash
)
from atomic_p2p.utils.logging import getLogger


class AtomicP2P(object):

    def __init__(self, role, addr, name, cert):
        cert_file, key_file = cssc(cert_dir=getcwd(), cert_file=cert,
                                   key_file=cert.replace('.pem', '.key'))

        self.logger = getLogger(__name__)

        hash_str = self_hash(path=join(getcwd(), 'atomic_p2p'))
        addr = addr.split(':') if type(addr) is str else addr

        self.services = {
            'peer': Peer(host=addr, name=name, role=role, _hash=hash_str,
                         cert=(cert_file, key_file))
        }
        self.services['monitor'] = self.services['peer'].monitor

    def start(self):
        for each in self.services:
            if self.services[each].is_start() is False:
                self.services[each].start()
        self.logger.info('Platform started.')

    def stop(self):
        for each in self.services:
            self.services[each].stop()

    def onProcess(self, cmd):
        if type(cmd) != list and type(cmd) == str:
            cmd = cmd.split(' ')

        service_key = cmd[0].lower()
        if service_key in self.services:
            return (True, self.services[service_key].onProcess(cmd[1:]))
        elif service_key in ['help', '?']:
            help_tips = 'peer help            - See peer\'s help\n'\
                        'monitor help        - See monitor\'s help\n'\
                        'exit/stop            - exit the whole program.\n'
            return (True, help_tips)
        elif service_key == 'monitor':
            return (True, self.services['peer'].onProcess(cmd[1:]))
        elif service_key == 'stop':
            self.stop()
            return (True, None)
        else:
            return (False, None)


def main(role, addr, target, name, cert, auto_start, auto_join_net,
         local_monitor_pass):

    logger = getLogger(add_monitor_pass=local_monitor_pass)
    atomic_p2p = AtomicP2P(role=role, addr=addr, name=name, cert=cert)

    if local_monitor_pass is not None:
        local_monitor = LocalMonitor(service=atomic_p2p,
                                     password=local_monitor_pass)
        atomic_p2p.services['local_monitor'] = local_monitor

    if auto_start is True:
        atomic_p2p.start()
    if auto_join_net is True and target is not None:
        if auto_start is False:
            atomic_p2p.start()
        atomic_p2p.onProcess(['peer', 'join', target])
