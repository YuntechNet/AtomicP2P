from ..Explainer import Explainer

class Executor:

    def __init__(self, con):
        self.con = con
        self.explainer = Explainer()

    def _execute_(self, msg):
        self.con.send_command(msg)
