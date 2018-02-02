from commands.Command import Command

class Exit(Command):

    reg = '^(exit)'

    def __init__(self):
        super().__init__()
