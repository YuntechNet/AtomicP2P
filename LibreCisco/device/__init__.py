from LibreCisco.device.device import Device
from LibreCisco.device.command import HelpCmd, AddCmd, RemoveCmd, ListCmd
from LibreCisco.device.trap_server import TrapServer
from LibreCisco.utils import printText
from LibreCisco.utils.manager import ProcManager

from pysnmp.hlapi.asyncore import SnmpEngine

class DeviceManager(ProcManager):

    def __init__(self, peer, loopDelay=60, output_field=None):
        self.peer = peer
        super(DeviceManager, self).__init__(loopDelay=loopDelay,
                                            output_field=output_field,
                                            auto_register=True)
        self.devices = []
        self._snmpEngine = SnmpEngine()
        # TODO: Temporary remove trapServer variable until fix the Permission-
        #       Denied error in Travis build when binding to 0.0.0.0:162.
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
        msg_key = msg_arr[0].lower()
        msg_arr = msg_arr[1:]
        if msg_key in self.commands:
            return self.commands[msg_key].onProcess(msg_arr)
        return ''

    def start(self):
        #self.trapServer.start()    # L18
        pass

    def stop(self):
        #self.trapServer.stop()     # L18
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
