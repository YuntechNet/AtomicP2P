import json, os

from Config import Config
from database.Database import TempDatabase
from database.Manager import RedisManager
from schedule.Schedule import Schedule
from utils.Manager import ProcessManager
from utils.User import User
from utils.Enums import UserPriority, LogLevel

# ScheduleManager
#   A process responsible for arrange schedule to execute with switch.
#
#class ScheduleManager(multiprocessing.Process):
class ScheduleManager(ProcessManager):

    def __init__(self, outputQueue, argv=None, sleep=60, callback=None):
        ProcessManager.__init__(self, 'ScheduleManager', outputQueue, callback)
        self.sleep = sleep

        if not self.loadConfig() or self.isExit():
            self.stopped.set()
            return
        self.print('Config loaded.')
        self.redisManager = RedisManager('ScheduleManager-Redis', ['ScheduleManager-Redis'], outputQueue, self.command)
        self.redisManager.start()

        self.schedules = {}
        self.user = User('system.scheduler', UserPriority.SCHEDULE)
        self.getScheduleFromLocal()
        self.print('Inited.', LogLevel.SUCCESS)

    def loadConfig(self):
        self.print('Loading config')
        if hasattr(Config, 'SCHEDULE_MANAGER'):
            self.config = Config.SCHEDULE_MANAGER
            if 'TEMP_DATABASE' in self.config:
                self.tempDB = TempDatabase(self.outputQueue, self.config['TEMP_DATABASE'])
            return True
        else:
            self.print('Config must contain SCHEDULE_MANAGER attribute.', LogLevel.ERROR)
            return False

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

    def getScheduleFromLocal(self):
        schedulesInDB = self.tempDB.execute('SELECT * FROM `Schedule`').fetchall()
        for (name, jsonContent) in schedulesInDB:
            self.schedules[name] = Schedule(self, name, self.outputQueue, json.loads(jsonContent))
            self.schedules[name].start()

    def getScheduleByName(self, name):
        for (key, value) in self.schedules.items():
            if value.name == name:
                return self.schedules[key]

    def command(self, command): #Override
        if super(ScheduleManager, self).command(command) is False and self.redisManager.isMine(command):
            if 'ls' in command._content:
                [self.print('%s %s' % (key, value)) for (key, value) in self.schedules.items()]
            elif 'load-folder' in command:
                [value.exit() for (key, value) in self.schedules.items()]
                self.loadFolder(overwrite='-force' in command._content)
            elif 'start-all' in command._content:
                [value.start() for (key, value) in self.schedules.items()]
            elif 'stop-all' in command._content:
                [value.exit() for (key, value) in self.schedules.items()]
            else:
                self.redisManager.print(command.to())

    def run(self):
        while not self.stopped.wait(self.sleep):
            pass

    def exit(self):
        for (name, instance) in self.schedules.items():
            instance.exit()
        self.redisManager.exit()
        super(ScheduleManager, self).exit()

