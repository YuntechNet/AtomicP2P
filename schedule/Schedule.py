import traceback, time
from threading import Event
from datetime import datetime, timedelta

from utils.Explainer import ScriptExplainer
from utils.Enums import LogLevel
from utils.Manager import ThreadManager

class Schedule(ThreadManager):

    def __init__(self, manager, name, outputQueue, json):
        ThreadManager.__init__(self, 'Schedule-%s' % name, outputQueue)
        try:
            self.target = json['target']
            self.startTime = datetime.fromtimestamp(json['startTime'])
            self.period = json['period']
            self.scriptExp = ScriptExplainer({
                'preCommand': json['preCommand'],
                'command': json['command']
            })
            self.sleep = int(self.period - (datetime.now() - self.startTime).total_seconds() % self.period)
            self.nextSchedule = manager.getScheduleByName(json['nextSchedule'])
            self.print(str(self.startTime) + '/' +  str(self.sleep) + '/' + str((datetime.now() - self.startTime).total_seconds()))
            self.print('Inited.', LogLevel.SUCCESS)
            return self
        except KeyError as keyErr:
            self.print('Init schedule failed: KeyError with missing %s' % keyErr, LogLevel.WARNING)
            return None
        except:
            traceback.print_exc()

    def start(self):
        super(Schedule, self).start()
        self.print('%s started.' % self.name)

    def run(self):
        while not self.stopped.wait(self.sleep):
            for each in self.command:
                exec(each)
            self.sleep = self.period

class NextSchedule:
    
    def __init__(self, json):
        self.command = json['command']
        self.delay = int(json['delay']) if 'delay' in json else 0
        self.nextSchedule = json['nextSchedule']

    def run(self):
        time.sleep(self.delay)
        for each in self.command:
            exec(each)
