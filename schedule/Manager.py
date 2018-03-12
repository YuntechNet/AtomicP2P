import json

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
        self.loadSchedules()
        self.print('Inited.')

    def loadSchedules(self):
        schedulesInDB = self.tempDB.execute('SELECT * FROM `Schedule`').fetchall()
        for (name, jsonContent) in schedulesInDB:
            self.schedules[name] = json.loads(jsonContent)

    def run(self):
        while not self.stopped.wait(self.sleep):
            pass
