from pydofus2.com.ankamagames.dofus.misc.utils.AbstractAction import AbstractAction
from pydofus2.com.ankamagames.jerakine.handlers.messages.Action import Action


class ServerSelectionAction(AbstractAction, Action):

    serverId: int

    def __init__(self, *params):
        super().__init__(*params)

    @classmethod
    def create(cls, serverId: int, *args) -> "ServerSelectionAction":
        a = cls(args)
        a.serverId = serverId
        return a
