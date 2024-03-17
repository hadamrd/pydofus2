import sys

from pydofus2.com.ankamagames.dofus.misc.utils.AbstractAction import \
    AbstractAction
from pydofus2.com.ankamagames.jerakine.handlers.messages.Action import Action


class FinishMoveSetRequestAction(AbstractAction, Action):

    enabledFinishedMoves: list[int]

    disabledFinishedMoves: list[int]

    def __init__(self, params: list = None):
        super().__init__(params)

    @classmethod
    def create(cls, enabledFinishedMoves: list[int], disabledFinishedMoves: list[int]) -> "FinishMoveSetRequestAction":
        action = cls(sys.argv[1:])
        action.enabledFinishedMoves = enabledFinishedMoves
        action.disabledFinishedMoves = disabledFinishedMoves
        return action
