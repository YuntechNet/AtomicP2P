
from network.commands.Command import Command

class Status:

    @staticmethod
    def req(redis, _to='Status', _data=None):
        redis.print(redis.instance['statusManager'].status)
        return None

    @staticmethod
    def res(redis, cmd):
        return None
