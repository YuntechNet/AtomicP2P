import logging

from network.commands.Command import Command
from status.commands.HeartBeat import HeartBeat

class Online:

    @staticmethod
    def req(redis, _to='Status', _data=None):
        Command(redis.name, _to, '--status online', _data).send(redis)
        return None

    @staticmethod
    def res(redis, cmd):
        redis.instance['statusManager'].markStatus(cmd._from, True)
        redis.print('%s is online' % cmd._from, logging.DEBUG)
        if redis.name != cmd._from:
            HeartBeat.req(redis, cmd._from)
        return None
