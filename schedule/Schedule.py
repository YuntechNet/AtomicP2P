import threading
from threading import Event
from datetime import datetime, timedelta

class Schedule(threading.Thread):

    def __init__(self, json):
        threading.Thread.__init__(self)
        self.startTime = datetime.fromtimestamp(json['startTime'])
        self.period = int(json['period'])
        self.preCommand = json['preCommand']
        self.command = json['command']
        self.stopped = Event()
        self.sleep = 0

    # Method to count sleep time to next trigger point.
    #   formula: period - (now - start) / period = now to next trigger point offset.
    def countSleep(self):
        return self.period - (datetime.now() - self.startTime).total_seconds() / self.period

    def run(self):
        self.sleep = countSleep()
        while not self.stopped.wait(self.sleep):
            print('test')
            self.sleep = countSleep()
