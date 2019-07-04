from traceback import format_exc


class Command(object):

    def __init__(self, cmd: str, **kwargs):
        """Init of Command class

        Args:
            cmd: unique key for command.
        """
        self.cmd = cmd

    def _on_command_recv(self, msg_arr: list, **kwargs) -> str:
        """Precheck when command is trigger

        Args:
            msg_arr: command with arguments split into array.
        
        Returns:
            command's process result.
            Any exception will cause command annotations been print.
        """
        try:
            result = self._execute(msg_arr, **kwargs)
            if result is None:
                return "Command Done"
            else:
                return result
        except IndexError:
            if self.__doc__ is not None:
                return self.__doc__
            else:
                error_text = \
                    "==========\n" \
                    "Here is Command's __doc__.\n" \
                    " if you are executing some command " \
                    ", but this message shows.\n" \
                    " it mean the command don't have approriate __doct__.\n" \
                    "Make sure there is __doc__ in {{{}}} command class.\n" \
                    "=========="
                return error_text.format(self.cmd)
        except Exception:
            return format_exc()

    def _execute(self, msg_arr, **kwargs):
        """Implementation of each subclass, this defines how the command actual work"""
        raise NotImplementedError
