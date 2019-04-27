from typing import List


class Command(object):

    def __init__(self, cmd: str, **kwargs) -> None:
        self.cmd = cmd

    def onProcess(self, msg_arr: List, **kwargs) -> str:
        raise NotImplementedError
