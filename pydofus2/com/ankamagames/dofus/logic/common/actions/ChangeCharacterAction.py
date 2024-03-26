from pydofus2.com.ankamagames.dofus.misc.utils import AbstractAction
from pydofus2.com.ankamagames.jerakine.handlers.messages import Action


class ChangeCharacterAction(AbstractAction, Action):
    def __init__(self, params=None):
        super().__init__(params)
        self.serverId = 0

    @staticmethod
    def create(serverId, *args):
        a = ChangeCharacterAction(args)
        a.serverId = serverId
        return a
