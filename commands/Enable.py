from commands.Command import Command

class Enable(Command):

    reg = '^(en){1}(able)?'

    def __init__(self):
        super().__init__()
