from threading import Event
import multiprocessing
import threading, time

from Config import Config
from switch.Switch import Switch
from database.Database import TempDatabase
from database.Manager import RemoteDBManager

#class SwitchManager(multiprocessing.Process):
class SwitchManager(threading.Thread):

    def __init__(self, sleep=60):
        threading.Thread.__init__(self)
        self.stopped = Event()
        self.sleep = sleep

        if not self.loadConfig() or self.stopped.isSet():
            self.stopped.set()

    def print(self, msg):
        print('[SwitchManager] %s' % msg)

    def loadConfig(self):
        if hasattr(Config, 'SWITCH_MANAGER'):
            self.device = []
            self.config = Config.SWITCH_MANAGER
            if 'TEMP_DATABASE' in self.config:
                self.tempDB = TempDatabase(self.config['TEMP_DATABASE'])
            if 'STATIC' in self.config:
                for each in self.config['STATIC']:
                    self.device.append(Switch(each))
                self.print('STATIC devices loaded.')
            if 'DATABASE' in self.config and self.tempDB is not None:
                self.remoteDBManager = RemoteDBManager(self.tempDB, self.config['DATABASE'])
                self.remoteDBManager.start()
            
            return True
        else:
            self.print('Config must contain SWITCH_MANAGER attribute.')
            return False

    def run(self):
        while not self.stopped.wait(self.sleep):
            pass
