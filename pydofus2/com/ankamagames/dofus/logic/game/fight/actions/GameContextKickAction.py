from sys import argv

from pydofus2.com.ankamagames.dofus.misc.utils.AbstractAction import AbstractAction
from pydofus2.com.ankamagames.jerakine.handlers.messages.Action import Action


class GameContextKickAction(AbstractAction, Action):

    targetId: float

    def __init__(self, params: list = None):
        super().__init__(params)

    @classmethod
    def create(cls, targetId: float) -> "GameContextKickAction":
        a: GameContextKickAction = GameContextKickAction(argv)
        a.targetId = targetId
        return a
