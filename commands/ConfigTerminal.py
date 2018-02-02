from commands.Command import Command

class ConfigTerminal(Command):
    
    reg = '^conf{1}(igure)? {1}ter{1}(minal)?'

    def __init__(self):
        super().__init__()
