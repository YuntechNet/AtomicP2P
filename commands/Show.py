from commands.Command import Command

class Show(Command):
    
    reg = '^(show)'

    def __init__(self):
        super().__init__()
        self.args = [
            
        ]
