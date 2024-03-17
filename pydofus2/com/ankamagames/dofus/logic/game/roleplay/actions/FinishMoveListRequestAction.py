import sys

from pydofus2.com.ankamagames.dofus.misc.utils.AbstractAction import \
    AbstractAction
from pydofus2.com.ankamagames.jerakine.handlers.messages.Action import Action


class FinishMoveListRequestAction(AbstractAction, Action):
    def __init__(self, params: list = None):
        super().__init__(params)

    @classmethod
    def create(cls) -> "FinishMoveListRequestAction":
        return cls(sys.argv[1:])
