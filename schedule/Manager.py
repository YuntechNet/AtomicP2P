import json, os

from utils.Manager import ProcessManager
from utils.User import User
from utils.Enums import UserPriority

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
        self.print('Inited.')

    def getScheduleFromLocal(self):
        schedulesInDB = self.tempDB.execute('SELECT * FROM `Schedule`').fetchall()
        for (name, jsonContent) in schedulesInDB:
            self.schedules[name] = json.loads(jsonContent)

    def loadFolder(self, path=None, overwrite=False):
        path = path if path else './schedule/static/'
        for each in os.listdir(path if path else './schedule/static/'):
            if os.path.isfile(path + each):
                fileConn = open(path + each)
                jsonContent = fileConn.read()

                if not each in self.schedules:
                    self.schedules[each] = json.loads(jsonContent)
                    self.tempDB.execute('INSERT INTO `Schedule`(Name, content) VALUES (\'%s\', \'%s\');' % (each, jsonContent.replace('\'', '\'\'')))
                    self.print('%s%s New schedule loaded and inserted into database.' % (path, each))
                elif overwrite:
                    self.schedules[each] = json.loads(jsonContent)
                    self.tempDB.execute('UPDATE `Schedule` SET content = \'%s\' WHERE Name = \'%s\';' % (jsonContent.replace('\'', '\'\''), each))
                    self.print('%s%s Old schedule loaded and updated into database.' % (path, each))
                else:
                    self.print('%s%s Schedule is exists, abort. add -force to overwrite.' % (path, each))
                fileConn.close()
            else:
                self.print('%s%s folder detected, ignore.' % (path, each))

    def command(self, command): #Override
        if 'ls' in command:
            [self.print('%s %s' % (key, value)) for (key, value) in self.schedules.items()]
        elif 'load-folder' in command:
            self.loadFolder(overwrite='-force' in command)

    def run(self):
        while not self.stopped.wait(self.sleep):
            pass

