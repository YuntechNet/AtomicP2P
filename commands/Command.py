import time
from enums.SwitchMode import SwitchMode

class Command:

    reg = None
    mode = SwitchMode.DEFAULT

    def __init__(self):
        self.name = ''
        self.args = ''

    def _insert_(self, args):
        self.args = args[len(self.name) + 1:]
        return self

    def _execute_(self, executor, short=True, debug=False):
        if self.mode == SwitchMode.EN_CONF or self.mode == executor.mode:
            self.__pre_execute__(executor)
            executor.con.sendCommand('%s %s' % (self.name, self.args), wrap=True)
            result = executor.con.shell.recv(65535).decode('utf-8')
            while('#' not in result and '>' not in result):
                if ' --More--' in result:
                    result = result.replace(' --More-- ', '') + executor.con.send_command('q' if short else ' ', wrap=False)
                else:
                    result += executor.con.shell.recv(65535).decode('utf-8')
        else:
            print('Error switch mode, maybe you need en(enable) or conf ter(configure terminal)?')
        self.__post_execute__(executor)
        if debug:
            print(result)
        return (executor, result)

    # private method for extended command class to override to pre-operate with executor.
    def __pre_execute__(self, exe):
        pass

    # private method for extended class to override to post-operate with executor.
    def __post_execute__(self, exe):
        pass
