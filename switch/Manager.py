from threading import Event
import multiprocessing
import threading, time

from Config import Config
from switch.Switch import Switch
from database.Database import TempDatabase
from database.Manager import RemoteDBManager

#class SwitchManager(multiprocessing.Process):
class SwitchManager(threading.Thread):

    def __init__(self, msgQueue, sleep=1):
        threading.Thread.__init__(self)
        self.msgQueue = msgQueue
        self.stopped = Event()
        self.sleep = sleep

        if not self.loadConfig() or self.stopped.isSet():
            self.stopped.set()
        self.print('Config loaded.')

    def print(self, msg):
        self.msgQueue.put(('[SwitchManager] %s' % msg, time.time()))

    def loadConfig(self):
        self.print('Loading config about SWITCH_MANAGER')
        if hasattr(Config, 'SWITCH_MANAGER'):
            self.device = []
            self.config = Config.SWITCH_MANAGER
            if 'TEMP_DATABASE' in self.config:
                self.tempDB = TempDatabase(self.msgQueue, self.config['TEMP_DATABASE'])
            if 'STATIC' in self.config:
                for each in self.config['STATIC']:
                    self.device.append(Switch(each))
                self.print('STATIC devices loaded.')
            if 'DATABASE' in self.config and self.tempDB is not None:
                self.remoteDBManager = RemoteDBManager(self.msgQueue, self.tempDB, self.config['DATABASE'])
                self.remoteDBManager.start()
            return True
        else:
            self.print('Config must contain SWITCH_MANAGER attribute.')
            return False

    def getDeviceFromLocal(self):
        if self.remoteDBManager.remoteDB.type == 'mongodb':
            from bson.json_util import loads as bsonLoads
        self.devices = []
        exe = self.tempDB.execute('SELECT * FROM `Switch`')
        result = exe.fetchall()
        for each in result:
            config = bsonLoads(each[1])
            config['host'] = each[0]
            self.devices.append(Switch(config))

    def run(self):
        while not self.stopped.wait(self.sleep):
            self.getDeviceFromLocal()
