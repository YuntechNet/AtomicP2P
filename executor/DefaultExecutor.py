from Executor import Executor

class DefaultExecutor(Executor):

    def __init__(self, con):
        super().__init__(con)
        self.commands = [
            'exit'
        ]
