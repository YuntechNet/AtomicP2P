
from LibreCisco.utils.manager import ProcManager


class SwitchManager(ProcManager):

    def __init__(self, peer, loopDelay=1, output_field=None):
        super(SwitchManager, self).__init__(loopDelay=loopDelay,
                                            ouput_field=output_field)
        self.peer = peer

    def registerHandler(self):
        pass

    def registerCommand(self):
        pass

    def run(self):
        while not self.stopped.wait(self.loopDelay):
            pass
