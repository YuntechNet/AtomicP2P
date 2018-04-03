import logging, json, os

from Config import Config
from database.Manager import DatabaseManager
from network.Manager import RedisManager
from schedule.Schedule import Schedule
from utils.Manager import ProcessManager
from utils.User import User
from utils.Enums import UserPriority, CommandType

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

    def __init__(self, outputQueue, argv=None, sleep=60, config=Config):
        ProcessManager.__init__(self, 'ScheduleManager', outputQueue)
        self.sleep = sleep

        if not self.loadConfig(config) or self.isExit():
            self.stopped.set()
            return
        self.print('Config loaded.')

        self.schedules = {}
        self.user = User('system.scheduler', UserPriority.SCHEDULE)
        self.toSystem()
        self.scheduleStart()
        self.print('Inited.', logging.INFO)

    def start(self, instance):
        self.instance = instance
        self.databaseManager.start()
        super(ScheduleManager, self).start()

    def loadConfig(self, config=Config):
        self.print('Loading config')
        if hasattr(config, 'SCHEDULE_MANAGER'):
            self.config = config.SCHEDULE_MANAGER
            self.databaseManager = ScheduleDatabaseManager(self.outputQueue, self.config)
            return True
        else:
            self.print('Config must contain SCHEDULE_MANAGER attribute.', logging.ERROR)
            return False

    def openFile(self, filePath):
        with open(filePath, encoding='utf-8') as fileConn:
            jsonStr = fileConn.read()
            jsonContent = json.loads(jsonStr)
            select = self.databaseManager.temporDB.execute('SELECT * FROM `Schedule` WHERE NAME=\'%s\';' % jsonContent['name']).fetchall()

            if select == []:
                self.databaseManager.temporDB.execute('INSERT INTO `Schedule`(Name, content) VALUES (\'%s\', \'%s\');' % (jsonContent['name'], json.dumps(jsonContent).replace('\'', '\'\'')))
                self.print('%s New schedule %s loaded and inserted into database.' % (filePath, jsonContent['name']))
            else:
                self.databaseManager.temporDB.execute('UPDATE `Schedule` SET content = \'%s\' WHERE Name = \'%s\';' % (json.dumps(jsonContent).replace('\'', '\'\''), jsonContent['name']))
                self.print('%s Old schedule %s loaded and updated into database.' % (filePath, jsonContent['name']))

    def loadFolder(self, path=None, overwrite=False, immediate=False):
        path = path if path else './schedule/static/'
        if os.path.isfile(path):
            self.openFile(path)
        else:
            for filename in os.listdir(path):
                if os.path.isfile(path + filename):
                    self.openFile(path + filename)
                else:
                    self.print('%s%s folder detected, ignore.' % (path, filename))
        self.toSystem(immediate=immediate)

    def toSystem(self, immediate=False):
        schedulesInDB = self.databaseManager.temporDB.execute('SELECT * FROM `Schedule`').fetchall()
        for (name, jsonContent) in schedulesInDB:
            if name in self.schedules:
                if immediate:
                    self.schedules[name].exit()
                    self.schedules[name] = Schedule(self, self.outputQueue, json.loads(jsonContent))
                else:
                    self.schedules[name].update(json.loads(jsonContent))
            else:
                self.schedules[name] = Schedule(self, self.outputQueue, json.loads(jsonContent))

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
        for (name, schedule) in self.schedules.copy().items():
            schedule.exit()
        self.databaseManager.exit()
        super(ScheduleManager, self).exit()

