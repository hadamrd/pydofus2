from sys import argv

from pydofus2.com.ankamagames.dofus.misc.utils.AbstractAction import AbstractAction
from pydofus2.com.ankamagames.jerakine.handlers.messages.Action import Action


class GameFightPlacementSwapPositionsAcceptAction(AbstractAction, Action):

    requestId: int

    def __init__(self, params: list = None):
        super().__init__(params)

    @classmethod
    def create(cls, pRequestId: int) -> "GameFightPlacementSwapPositionsAcceptAction":
        action: GameFightPlacementSwapPositionsAcceptAction = GameFightPlacementSwapPositionsAcceptAction(argv)
        action.requestId = pRequestId
        return action
