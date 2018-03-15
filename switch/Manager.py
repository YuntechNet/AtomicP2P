import queue

from Config import Config
from utils.Enums import LogLevel
from utils.Manager import ProcessManager
from switch.Switch import Switch
from database.Database import TempDatabase
from database.Manager import RemoteDBManager

# SwitchManager
#   A process responsible for arrane switch heart-beat & execute command.
#
class SwitchManager(ProcessManager):

    def __init__(self, outputQueue, sleep=1):
        ProcessManager.__init__(self, 'SwitchManager', outputQueue)
        self.sleep = sleep

        if not self.loadConfig() or self.isExit():
            self.stopped.set()
        self.print('Config loaded.', LogLevel.SUCCESS)
        self._makeQueue_()
        self.print('Inited.', LogLevel.SUCCESS)

    def loadConfig(self):
        self.print('Loading config')
        if hasattr(Config, 'SWITCH_MANAGER'):
            self.device = []
            self.config = Config.SWITCH_MANAGER
            self.address = self.config['ADDRESS']
            if 'TEMP_DATABASE' in self.config:
                self.tempDB = TempDatabase(self.outputQueue, self.config['TEMP_DATABASE'])
            if 'STATIC' in self.config:
                for each in self.config['STATIC']:
                    self.device.append(Switch(each))
                self.print('STATIC devices loaded.', LogLevel.SUCCESS)
            if 'DATABASE' in self.config and self.tempDB is not None:
                self.remoteDBManager = RemoteDBManager(self.outputQueue, self.tempDB, self.config['DATABASE'])
                self.remoteDBManager.start()
            return True
        else:
            self.print('Config must contain SWITCH_MANAGER attribute.', LogLevel.ERROR)
            return False

    def getDeviceFromLocal(self):
        if self.remoteDBManager.remoteDB.type == 'mongodb':
            from bson.json_util import loads as bsonLoads
        self.devices = []
        result = self.tempDB.execute('SELECT * FROM `Switch`').fetchall()
        for (host, jsonContent) in result:
            config = bsonLoads(jsonContent)
            config['host'] = host
            self.devices.append(Switch(config))

    def getDeviceByHost(self, host):
        for each in self.device:
            if each.config.host == host:
                return each
        return None

    def run(self):
        while not self.stopped.wait(self.sleep):
            self.getDeviceFromLocal()

    def exit(self):
        self.remoteDBManager.exit()
        super(SwitchManager, self).exit()
