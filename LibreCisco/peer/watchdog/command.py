from LibreCisco.peer.watchdog.peer_status import StatusType
from LibreCisco.utils import printText
from LibreCisco.utils.command import Command


class HelpCmd(Command):
    """HelpCmd
        show the help for watchdog.
        Usage in prompt: watchdog help [cmd]
    """

    def __init__(self, watchdog):
        super(HelpCmd, self).__init__('help')
        self.watchdog = watchdog
        self.peer = watchdog.peer
        self.output_field = self.peer.output_field

    def onProcess(self, msg_arr):
        if msg_arr != [] and msg_arr[0] in self.watchdog.commands:
            printText(self.watchdog.commands[msg_arr[0]].__doc__)
        else:
            printText("watchdog [cmd] <options>\n"
                      " - pause                                          "
                      "pause watchdog's main loop thread.\n"
                      " - period [seconds]                               "
                      "change watchdog's loop period to another second.\n"
                      " - list                                           "
                      "list each statuses in list.\n"
                      " - reset [peer name/role/all]                     "
                      "reset all or specific name or role's peer status t"
                      "o PENDING.")


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
        except ValueError:
            printText('Please input a integer: {}'.format(msg_arr[0]))
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
            printText('There is the status list of peers in current net:')
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
        if msg_arr == []:
            for each in self.watchdog.watchdoglist:
                each.update(status_type=StatusType.PENDING)
        else:
            pass


class VerboseCmd(Command):
    """VerboseCmd
        toggle verbose flag in watchdog to output more detail or not.
        Usage in prompt: watchdog verbose
    """

    def __init__(self, watchdog):
        super(VerboseCmd, self).__init__('verbose')
        self.watchdog = watchdog
        self.peer = watchdog.peer
        self.output_field = self.peer.output_field

    def onProcess(self, msg_arr):
        self.watchdog.verbose = not self.watchdog.verbose
        printText('Watchdog verbose toggle to: {}'.format(
                        self.watchdog.verbose))


class ManualCmd(Command):
    """ManualCmd
        manually to send a check pkt to specific peer.
        Usage in prompt: watchdog manuadl [ip:port]
    """

    def __init__(self, watchdog):
        super(ManualCmd, self).__init__('manual')
        self.watchdog = watchdog
        self.peer = watchdog.peer
        self.output_field = self.peer.output_field

    def onProcess(self, msg_arr):
        host = msg_arr[0].split(':')
        self.peer.sendMessage((host[0], host[1]), 'watchdog_check')
        if self.watchdog.verbose:
            printText('Sended a watchdog check to: {}'.format(host))
