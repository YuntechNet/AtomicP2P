from atomic_p2p.communication import Command


class CommandableMixin(object):
    """CommandableMixin for anything which needs command ability.
    The class inherits this mixin, should contains a dict named to commands.

    Attributes:
        commands: dict variable to stroe / register commands.
    """

    def register_command(self, command: "Command", force: bool = False) -> bool:
        """Register the command with it's cmd to commands

        Args:
            command: The command to be register.
            force: If command is exists, whether override it or not.

        Returns:
            True if command been set, False is fail.
        """
        if command.cmd not in self.commands or force is True:
            self.commands[command.cmd] = command
            return True
        return False

    def unregister_command(self, cmd: str) -> bool:
        """Unregister a command in commands

        Args:
            cmd: Target command's key cmd to unregister.

        Returns:
            True if remove success, False means not exists.
        """
        if cmd in self.commands:
            del self.commands[cmd]
            return True
        return False

    # Temporary support old calling. Will be deprecate soon. 2019/04/26
    def onProcess(self, msg_arr, **kwargs) -> str:
        self.logger.warning(
            "[Deprecated] onProcess method is no longer maintai"
            "n, manually send command into peer is not recommended."
        )
        return self._on_command(msg_arr, **kwargs)

    def _on_command(self, msg_arr: list, **kwargs) -> str:
        try:
            msg_key = msg_arr[0].lower()
            msg_arr = msg_arr[1:]
            if msg_key in self.commands:
                return self.commands[msg_key]._on_command_recv(msg_arr)
            return self.commands["help"]._on_command_recv(msg_arr)
        except Exception:
            return self.commands["help"]._on_command_recv(msg_arr)
