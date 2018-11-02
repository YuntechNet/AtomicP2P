from os import getcwd
from os.path import join
from LibreCisco.peer import Peer
from LibreCisco.utils import printText
from LibreCisco.utils.security import (
    create_self_signed_cert as cssc, self_hash
)


class LibreCisco(object):

    def __init__(self, role, addr, target, name, cert, dashboard_field,
                 peer_field, auto_start=False, auto_join_net=False):
        cert_file, key_file = cssc(cert_dir=getcwd(), cert_file=cert,
                                   key_file=cert.replace('.pem', '.key'))
        hash_str = self_hash(path=join(getcwd(), 'LibreCisco'))
        addr = addr.split(':') if type(addr) is str else addr

        self.output_field = dashboard_field
        self.services = {
            'peer': Peer(host=addr, name=name, role=role, _hash=hash_str,
                         cert=(cert_file, key_file),
                         output_field=[dashboard_field, peer_field])
        }

        if auto_start:
            self.start()
        if auto_join_net and target is not None:
            if auto_start is False:
                self.start()
            self.services['peer'].onProcess(['join', target])

    def start(self):
        for each in self.services:
            self.services[each].start()

    def stop(self):
        for each in self.services:
            self.services[each].stop()

    def onProcess(self, cmd):
        if type(cmd) != list and type(cmd) == str:
            cmd = cmd.split(' ')

        service_key = cmd[0].lower()
        if service_key in self.services:
            self.services[service_key].onProcess(cmd[1:])
        elif service_key == 'monitor':
            self.services['peer'].onProcess(cmd[1:])
        elif service_key == 'stop':
            self.stop()
        else:
            return False
        return True
