

class Command(object):

    def __init__(self, cmd, **kwargs):
        self.cmd = cmd

    def onProcess(self, msg_arr, **kwargs):
        raise NotImplementedError
