from typing import Union
from inspect import currentframe

from ..communication import Handler


class HandleableMixin(object):
    """HandleableMixin for anything which needs handle ability.
    The class which needs communication through Peer class should inherits this
     mixin, and contains a dict named pkt_handlers.

    Attributes:
        pkt_handlers: dict variable to stroe / register handles.
    """

    def register_handler(self, handler: "Handler", force: bool = False) -> bool:
        """Register the handler with it's pkt_type to pkt_handlers

        Args:
            handler: The handler to be register.
            force: If handler is exists, whether override it or not.

        Returns:
            True if handler been set, False is fail.
        """
        if handler.pkt_type not in self.pkt_handlers or force is True:
            self.pkt_handlers[type(handler).pkt_type] = handler
            return True
        return False

    def unregister_handler(self, pkt_type: str) -> bool:
        """Unregister a handler in pkt_handlers

        Args:
            pkt_type: Target handler's pkt_type to unregister.

        Returns:
            True if remove success, False means not exists.
        """
        if pkt_type in self.pkt_handlers:
            del self.pkt_handlers[pkt_type]
            return True
        return False

    def select_handler(self, pkt_type: str) -> Union[None, "Handler"]:
        """select a handler with given packet handler type.
        If current class's pkt_handlers is not match, will iterate each va-
        riable which inherits HandleableMixin class. Also it will prevent 
        circular interact in case a instance that passing parent instance.

        Args:
            pkt_type: Target handler's pkt_type to get.

        Returns:
            Handler which match given pkt_type or None if not found.
        """
        if pkt_type in self.pkt_handlers:
            return self.pkt_handlers[pkt_type]
        else:
            for (_, val) in vars(self).items():
                if isinstance(val, HandleableMixin) is True:
                    if "self" in currentframe().f_back.f_locals:
                        return (
                            val.select_handler(pkt_type=pkt_type)
                            if (val != currentframe().f_back.f_locals["self"])
                            else None
                        )
                    return val.select_handler(pkt_type=pkt_type)
            return None
