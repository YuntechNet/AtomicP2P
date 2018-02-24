from Config import Config
from switch.Switch import Switch
from threading import Event
import threading, time

class SwitchManager(threading.Thread):

    def __init__(self, sleep=60):
        threading.Thread.__init__(self)
        self.stopped = Event()
        self.sleep = sleep

        self.device = []
        for each in Config.DEVICES:
            self.device.append(Switch(each))
        for each in self.device:
            each.initSwitch()

    def run(self):
        while not self.stopped.wait(self.sleep):
            for each in self.device:
                print('[%s] pined sw host %s with username %s and password %s' % (time.time, each.host, each.username, each.password))
