import traceback, time
from threading import Event
from datetime import datetime, timedelta

from utils.Explainer import ScriptExplainer
from utils.Enums import LogLevel
from utils.Manager import ThreadManager

class Type:

    def __int__(self, json):
        if 'text' in json:
            self.mode = 'text'
        elif 'count' in json:
            self.mode = 'count'
            self.time = json['count']
        elif 'cron' in json:
            self.mode = 'cron'
            self.time = json['cron']

class Schedule(ThreadManager):

    def __init__(self, manager, name, outputQueue, json):
        ThreadManager.__init__(self, 'Schedule-%s' % name, outputQueue)
        try:
            self.name = json['name']
            self.target = json['target']
            self.type = Type(json['type'])
            self.beforeScript = json['beforeScript']
            self.script = json['script']
            self.nextSchedule = manager.getScheduleByName(json['nextSchedule'])
            self.sleep = 0
            self.print('Inited.', LogLevel.SUCCESS)
            return self
        except KeyError as keyErr:
            self.print('Init schedule failed: KeyError with missing %s' % keyErr, LogLevel.WARNING)
            return None
        except:
            traceback.print_exc()
            return None

    def calSleep(self):
        if self.type.mode == 'count':
            return self.type.time
        elif self.type.mode == 'cron':
            return (datetime.now() - datetime.strptime('%H:%M:%S', self.type.time)).total_seconds()

    def start(self):
        if self.type.mode == 'text':
            pass
        else:
            self.sleep = self.calSleep()
        super(Schedule, self).start()

        self.print('%s started.' % self.name)

    def run(self):
        while not self.stopped.wait(self.sleep):
            pass
            self.sleep = self.calSleep()

class NextSchedule:
    
    def __init__(self, json):
        self.command = json['command']
        self.delay = int(json['delay']) if 'delay' in json else 0
        self.nextSchedule = json['nextSchedule']

    def run(self):
        time.sleep(self.delay)
        for each in self.command:
            exec(each)
