from LibreCisco.peer.entity.peer_status import StatusType
from LibreCisco.utils import printText
from LibreCisco.utils.command import Command


class HelpCmd(Command):
    """HelpCmd
        show the help for monitor.
        Usage in prompt: monitor help [cmd]
    """

    def __init__(self, monitor):
        super(HelpCmd, self).__init__('help')
        self.monitor = monitor
        self.peer = monitor.peer
        self.output_field = self.peer.output_field

    def onProcess(self, msg_arr):
        if msg_arr != [] and msg_arr[0] in self.monitor.commands:
            printText(self.monitor.commands[msg_arr[0]].__doc__)
        else:
            printText("monitor [cmd] <options>\n"
                      " - pause                                          "
                      "pause monitor's main loop thread.\n"
                      " - period [seconds]                               "
                      "change monitor's loop period to another second.\n"
                      " - list                                           "
                      "list each statuses in list.\n"
                      " - reset [peer name/role/all]                     "
                      "reset all or specific name or role's peer status t"
                      "o PENDING.")


class PauseCmd(Command):
    """PauseCmd
        pause monitor keep checking peers.
        Usage in prompt: monitor pause
    """

    def __init__(self, monitor):
        super(PauseCmd, self).__init__('pause')
        self.monitor = monitor
        self.peer = monitor.peer
        self.output_field = self.peer.output_field

    def onProcess(self, msg_arr):
        self.monitor.pause = not self.monitor.pause
        printText('Monitor pause: {}'.format(self.monitor.pause))


class PeriodCmd(Command):
    """PeriodCmd
        adjust monitor's checking delay in seconds.
        Usage in prompt: monitor period [seconds]
    """

    def __init__(self, monitor):
        super(PeriodCmd, self).__init__('period')
        self.monitor = monitor
        self.peer = monitor.peer
        self.output_field = self.peer.output_field

    def onProcess(self, msg_arr):
        try:
            period = int(msg_arr[0])
            self.monitor.loopDelay = period
            printText('Monitor check sending period \
                       change to: {} seconds.'.format(period))
        except ValueError:
            printText('Please input a integer: {}'.format(msg_arr[0]))
        except Exception as e:
            printText(e)


class ListCmd(Command):
    """ListCmd
        list all peer status in list
        Usage in prompt: monitor list
    """

    def __init__(self, monitor):
        super(ListCmd, self).__init__('list')
        self.monitor = monitor
        self.peer = monitor.peer
        self.output_field = self.peer.output_field

    def onProcess(self, msg_arr):
        if len(self.peer.connectlist) == 0:
            printText('There is no peer\'s info in current list')
        else:
            printText('There is the status list of peers in current net:')
            for each in self.peer.connectlist:
                printText(' - {} / {}'.format(each.status, each))
            printText('[---End of list---]')


class ResetCmd(Command):
    """ResetCmd
        reset specific or every peer's status in monitor's list.
        Usage in prompt: monitor reset all
    """

    def __init__(self, monitor):
        super(ResetCmd, self).__init__('reset')
        self.monitor = monitor
        self.peer = monitor.peer

    def onProcess(self, msg_arr):
        if msg_arr == []:
            for each in self.peer.connectlist:
                each.status.update(status_type=StatusType.PENDING)
                printText(each.status)
            printText("Reset success")
        else:
            pass


class VerboseCmd(Command):
    """VerboseCmd
        toggle verbose flag in monitor to output more detail or not.
        Usage in prompt: monitor verbose
    """

    def __init__(self, monitor):
        super(VerboseCmd, self).__init__('verbose')
        self.monitor = monitor
        self.peer = monitor.peer
        self.output_field = self.peer.output_field

    def onProcess(self, msg_arr):
        self.monitor.verbose = not self.monitor.verbose
        printText('Monitor verbose toggle to: {}'.format(
                        self.monitor.verbose))


class ManualCmd(Command):
    """ManualCmd
        manually to send a check pkt to specific peer.
        Usage in prompt: monitor manuadl [ip:port]
    """

    def __init__(self, monitor):
        super(ManualCmd, self).__init__('manual')
        self.monitor = monitor
        self.peer = monitor.peer
        self.output_field = self.peer.output_field

    def onProcess(self, msg_arr):
        host = msg_arr[0].split(':')
        try:
            host[1] = int(host[1])
            self.peer.handler_unicat_packet(
                host=(host[0], host[1]), pkt_type='monitor_check')
        except ValueError:
            self.peer.handler_broadcast_packet(
                host=(host[0], host[1]), pkt_type='monitor_check')
        if self.monitor.verbose:
            printText('Sended a monitor check to: {}'.format(host))
