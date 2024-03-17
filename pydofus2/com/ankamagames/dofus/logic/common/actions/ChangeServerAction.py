from pydofus2.com.ankamagames.dofus.misc.utils.AbstractAction import \
    AbstractAction
from pydofus2.com.ankamagames.jerakine.handlers.messages.Action import Action


class ChangeServerAction(AbstractAction, Action):

    def __init__(self, params=None):
        super().__init__(params)
        self.serverId = 0

    @classmethod
    def create(cls, serverId, *args):
        a = cls(args)
        a.serverId = serverId
        return a