import json, os

from schedule.Schedule import Schedule
from utils.Manager import ProcessManager
from utils.User import User
from utils.Enums import UserPriority, LogLevel

# ScheduleManager
#   A process responsible for arrange schedule to execute with switch.
#
#class ScheduleManager(multiprocessing.Process):
class ScheduleManager(ProcessManager):

    def __init__(self, tempDB, outputQueue, sleep=60):
        ProcessManager.__init__(self, 'ScheduleManager', outputQueue)
        self.sleep = sleep

        self.tempDB = tempDB
        self.schedules = {}
        self.user = User('system.scheduler', UserPriority.SCHEDULE)
        self.getScheduleFromLocal()
        self.print('Inited.', LogLevel.SUCCESS)

    def getScheduleFromLocal(self):
        schedulesInDB = self.tempDB.execute('SELECT * FROM `Schedule`').fetchall()
        for (name, jsonContent) in schedulesInDB:
            self.schedules[name] = Schedule(name, self.outputQueue, json.loads(jsonContent))

    def loadFolder(self, path=None, overwrite=False):
        path = path if path else './schedule/static/'
        for filename in os.listdir(path if path else './schedule/static/'):
            if os.path.isfile(path + filename):
                fileConn = open(path + filename)
                jsonContent = fileConn.read()

                if not filename in self.schedules:
                    self.schedules[filename] = Schedule(filename, self.outputQueue, json.loads(jsonContent))
                    self.tempDB.execute('INSERT INTO `Schedule`(Name, content) VALUES (\'%s\', \'%s\');' % (filename, jsonContent.replace('\'', '\'\'')))
                    self.print('%s%s New schedule loaded and inserted into database.' % (path, filename))
                elif overwrite:
                    self.schedules[filename] = Schedule(filename, self.outputQueue, json.loads(jsonContent))
                    self.tempDB.execute('UPDATE `Schedule` SET content = \'%s\' WHERE Name = \'%s\';' % (jsonContent.replace('\'', '\'\''), filename))
                    self.print('%s%s Old schedule loaded and updated into database.' % (path, filename))
                else:
                    self.print('%s%s Schedule is exists, abort. add -force to overwrite.' % (path, filename))
                fileConn.close()
            else:
                self.print('%s%s folder detected, ignore.' % (path, filename))

    def command(self, command): #Override
        if 'ls' in command:
            [self.print('%s %s' % (key, value)) for (key, value) in self.schedules.items()]
        elif 'load-folder' in command:
            self.loadFolder(overwrite='-force' in command)

    def run(self):
        while not self.stopped.wait(self.sleep):
            pass

    def exit(self):
        for (name, instance) in self.schedules.items():
            instance.exit()
        super(ScheduleManager, self).exit()
