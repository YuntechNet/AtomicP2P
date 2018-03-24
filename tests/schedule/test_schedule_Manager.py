from queue import Queue

from Config import Config
from schedule.Manager import ScheduleManager

class TestScheduleManager:

    def test_init(self):
        manager = ScheduleManager(Queue())
        assert manager.sleep == 60
        assert manager.loadConfig({}) == False
        
