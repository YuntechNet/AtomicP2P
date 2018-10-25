from LibreCisco.utils import printText
from LibreCisco.utils.command import Command


class ResetCmd(Command):
    """ResetCmd
        reset specific or every peer's status in watchdog's list.
        Usage in prompt: watchdog reset all
    """

    def __init__(self, peer):
        super(ResetCmd, self).__init__('reset')
        self.peer = peer
        self.watchdog = watchdog

    def onProcess(self, msg_arr):
        pass
