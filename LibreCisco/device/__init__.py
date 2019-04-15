from LibreCisco.device.device import Device
from LibreCisco.device.command import HelpCmd, AddCmd, RemoveCmd, ListCmd
from LibreCisco.device.trap_server import TrapServer
from LibreCisco.utils.manager import ProcManager
from LibreCisco.utils.logging import getLogger

from pysnmp.hlapi.asyncore import SnmpEngine

class DeviceManager(ProcManager):

    def __init__(self, peer, loopDelay=60):
        self.peer = peer
        super(DeviceManager, self).__init__(
            loopDelay=loopDelay, auto_register=True,
            logger=getLogger(__name__))
        self.devices = []
        self._snmpEngine = SnmpEngine()
        #self.trapServer = TrapServer()

    def registerHandler(self):
        pass
#        self.peer.handlers.update({
#            'add': JoinHandler(self.peer, self),
#            'remove': RemoveHandler(self.peer, self)
#        })

    def registerCommand(self):
        self.commands = {
            'help': HelpCmd(self),
            'add': AddCmd(self),
            'remove': RemoveCmd(self),
            'list': ListCmd(self)
        }

    def onProcess(self, msg_arr, **kwargs):
        try:
            msg_key = msg_arr[0].lower()
            msg_arr = msg_arr[1:]
            if msg_key in self.commands:
                return self.commands[msg_key]._on_process(msg_arr)
            return self.commands['help']._on_process(msg_arr)
        except Exception as e:
            return self.commands['help']._on_process(msg_arr)

    def start(self):
        #self.trapServer.start()
        pass

    def stop(self):
        #self.trapServer.stop()
        self.stopped.set()

    def run(self):
        while not self.stopped.wait(self.loopDelay):
            pass

    def addDevice(self, device):
        if type(device) is Device and device not in self.devices:
            self.devices.append(device)
            if device.connect_type == 'snmp':
                device.snmp_v3_init()
            else:
                device.fetch_running_config()
                device.fetch_interface_status()
