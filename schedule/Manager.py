from threading import Event
import threading

from utils.User import User
from utils.Enums import UserPrority

# ScheduleManager
#   A process responsible for arrange schedule to execute with switch.
#
#class ScheduleManager(multiprocessing.Process):
class ScheduleManager(threading.Thread):

    def __init__(self, sleep=60):
        threading.Thread.__init__(self)
        self.stopped = Event()
        self.sleep = sleep

        self.user = User('system.scheduler', UserPriority.SCHEDULE)

    def run(self):
        while not self.stopped.wait(self.sleep):
            pass
