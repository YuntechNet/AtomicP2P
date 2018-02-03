import re
from Explainer import Explainer
from enums.SwitchMode import SwitchMode

class Executor:

    def __init__(self, con):
        self.con = con
        self.mode = SwitchMode.ENABLE if re.compile('#$').search(con.output[2:].decode('utf-8')) else SwitchMode.DEFAULT

    def _execute_(self, cmdInstance):
        print('Mode: %s, Command: %s' % (str(self.mode), cmdInstance))
        return cmdInstance._execute_(self)
