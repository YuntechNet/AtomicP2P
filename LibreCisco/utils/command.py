from traceback import format_exc


class Command(object):
    """Command
    """

    def __init__(self, cmd, **kwargs):
        self.cmd = cmd

    def _on_process(self, msg_arr, **kwargs):
        try:
            result = self.onProcess(msg_arr, **kwargs)
            if result is None:
                return 'Command Done'
            else:
                return result
        except IndexError:
            if self.__doc__ is not None:
                return self.__doc__
            else:
                error_text = \
                    '==========\n' \
                    'Here is Command\'s __doc__.\n' \
                    ' if you are executing some command ' \
                    ', but this message shows.\n' \
                    ' it mean the command don\'t have approriate __doct__.\n' \
                    'Make sure there is __doc__ in {{{}}} command class.\n' \
                    '=========='
                return error_text.format(self.cmd)
        except Exception as e:
            return format_exc()

    def onProcess(self, msg_arr, **kwargs):
        raise NotImplementedError
