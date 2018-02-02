from Explainer import Explainer
from enums.SwitchMode import SwitchMode

class Executor:

    def __init__(self, con):
        self.con = con
        self.mode = SwitchMode.DEFAULT

    def _execute_(self, cmdInstance):
        print('Mode: %s, Command: %s' % (str(self.mode), cmdInstance))
        return cmdInstance._execute_(self)
