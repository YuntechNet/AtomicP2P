class Command:

    reg = None

    def __init__(self):
        self.args = None

    def _execute_(self, con):
        con.send_command(self.command, True)
