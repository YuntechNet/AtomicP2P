import json, os

from Config import Config
from database.Manager import DatabaseManager
from network.Manager import RedisManager
from schedule.Schedule import Schedule
from schedule.Command import ScheduleCommand
from utils.Manager import ProcessManager
from utils.User import User
from utils.Enums import UserPriority, LogLevel, CommandType

class ScheduleDatabaseManager(DatabaseManager):

    def __init__(self, outputQueue, config, sleep=300):
        DatabaseManager.__init__(self, outputQueue, config, sleep)

    # Override
    def sync(self):
        pass

# ScheduleManager
#   A process responsible for arrange schedule to execute with switch.
#
class ScheduleManager(ProcessManager):

    def __init__(self, outputQueue, argv=None, sleep=60, callback=None, config=Config):
        ProcessManager.__init__(self, 'ScheduleManager', outputQueue, callback)
        self.sleep = sleep

        if not self.loadConfig(config) or self.isExit():
            self.stopped.set()
            return
        self.print('Config loaded.')
        self.commander = ScheduleCommand(self)
        self.redis = RedisManager('ScheduleManager-Redis', ['ScheduleManager-Redis'], outputQueue, self.commander.process)

        self.schedules = {}
        self.user = User('system.scheduler', UserPriority.SCHEDULE)
        self.toSystem()
        self.scheduleStart()
        self.print('Inited.', LogLevel.SUCCESS)

    def start(self):
        self.redis.start()
        self.databaseManager.start()
        super(ScheduleManager, self).start()

    def loadConfig(self, config):
        self.print('Loading config')
        if hasattr(config, 'SCHEDULE_MANAGER'):
            self.config = config.SCHEDULE_MANAGER
            self.databaseManager = ScheduleDatabaseManager(self.outputQueue, self.config)
            return True
        else:
            self.print('Config must contain SCHEDULE_MANAGER attribute.', LogLevel.ERROR)
            return False

    def loadFolder(self, path=None, overwrite=False):
        path = path if path else './schedule/static/'
        for filename in os.listdir(path):
            if os.path.isfile(path + filename):
                with open(path + filename, encoding='utf-8') as fileConn:
                    jsonStr = fileConn.read()
                    jsonContent = json.loads(jsonStr)
                    select = self.databaseManager.temporDB.execute('SELECT * FROM `Schedule` WHERE NAME=\'%s\';' % jsonContent['name']).fetchall()

                    if select == []:
                        self.databaseManager.temporDB.execute('INSERT INTO `Schedule`(Name, content) VALUES (\'%s\', \'%s\');' % (jsonContent['name'], json.dumps(jsonContent)))
                        self.print('%s%s New schedule %s loaded and inserted into database.' % (path, filename, jsonContent['name']))
                    else:
                        self.databaseManager.temporDB.execute('UPDATE `Schedule` SET content = \'%s\' WHERE Name = \'%s\';' % (json.dumps(jsonContent), jsonContent['name']))
                        self.print('%s%s Old schedule %s loaded and updated into database.' % (path, filename, jsonContent['name']))
            else:
                self.print('%s%s folder detected, ignore.' % (path, filename))
        self.toSystem()

    def toSystem(self):
        schedulesInDB = self.databaseManager.temporDB.execute('SELECT * FROM `Schedule`').fetchall()
        for (name, jsonContent) in schedulesInDB:
            if name in self.schedules:
                self.schedules[name].update(json.loads(jsonContent))
            else:
                schedule = Schedule(self, self.outputQueue, json.loads(jsonContent))
                self.schedules[name] = schedule

    def scheduleStart(self, name=None):
        if not name:
            [ value.start() for (key, value) in self.schedules.items() ]
        else:
            for (key, value) in self.schedules.items():
                if key in name:
                    value.start()

    def getScheduleByName(self, name):
        if not name:
            return None
        for (key, value) in self.schedules.items():
            if value.name == name:
                return self.schedules[key]

    def run(self):
        while not self.stopped.wait(self.sleep):
            pass

    def exit(self):
        for (name, schedule) in self.schedules.items():
            schedule.exit()
        self.redis.exit()
        self.databaseManager.exit()
        super(ScheduleManager, self).exit()

