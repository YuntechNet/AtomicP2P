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

    def _execute_(self, executor):
        if self.mode == SwitchMode.EN_CONF or self.mode == executor.mode:
            print(executor)
            self.__execute__(executor)
            result = executor.con.send_command('%s %s' % (self.name, self.args), True)
            #print(result)
        else:
            print('Error switch mode, maybe you need en(enable) or conf ter(configure terminal)?')
        return executor

    def __execute__(self, exe):
        pass
