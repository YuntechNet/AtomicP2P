
from queue import Queue

from switch.Manager import SwitchManager

class TestSwitchManager:

    def test_init(self):
        manager = SwitchManager(Queue())
        assert manager.sleep == 1
        assert manager.loadConfig({}) == False 
        assert self.getDeviceByHost(manager) == None
        self.exit(manager)
        assert manager.isExit() == True

    def getDeviceByHost(self, manager):
        return manager.getDeviceByHost('255.255.255.255')    
        
    def exit(self, manager):
        manager.exit()
