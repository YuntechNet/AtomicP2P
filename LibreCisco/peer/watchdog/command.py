from LibreCisco.utils import printText
from LibreCisco.utils.command import Command


class PauseCmd(Command):
    """PauseCmd
        pause watchdog keep checking peers.
        Usage in prompt: watchdog pause
    """

    def __init__(self, watchdog):
        super(PauseCmd, self).__init__('pause')
        self.watchdog = watchdog
        self.peer = watchdog.peer
        self.output_field = self.peer.output_field

    def onProcess(self, msg_arr):
        self.watchdog.pause = not self.watchdog.pause
        printText('Watchdog pause: {}'.format(self.watchdog.pause))


class PeriodCmd(Command):
    """PeriodCmd
        adjust watchdog's checking delay in seconds.
        Usage in prompt: watchdog period [seconds]
    """

    def __init__(self, watchdog):
        super(PeriodCmd, self).__init__('period')
        self.watchdog = watchdog
        self.peer = watchdog.peer
        self.output_field = self.peer.output_field

    def onProcess(self, msg_arr):
        try:
            period = int(msg_arr[0])
            self.watchdog.loopDelay = period
            printText('Watchdog check sending period \
                       change to: {} seconds.'.format(period))
        except Exception as e:
            printText(e)


class ListCmd(Command):
    """ListCmd
        list all peer status in list
        Usage in prompt: watchdog list
    """

    def __init__(self, watchdog):
        super(ListCmd, self).__init__('list')
        self.watchdog = watchdog
        self.peer = watchdog.peer
        self.output_field = self.peer.output_field

    def onProcess(self, msg_arr):
        if len(self.watchdog.watchdoglist) == 0:
            printText('There is no peer\'s info in current list')
        else:
            for each in self.watchdog.watchdoglist:
                printText(' - ' + str(each))
            printText('[---End of list---]')


class ResetCmd(Command):
    """ResetCmd
        reset specific or every peer's status in watchdog's list.
        Usage in prompt: watchdog reset all
    """

    def __init__(self, watchdog):
        super(ResetCmd, self).__init__('reset')
        self.watchdog = watchdog
        self.peer = watchdog.peer

    def onProcess(self, msg_arr):
        pass
