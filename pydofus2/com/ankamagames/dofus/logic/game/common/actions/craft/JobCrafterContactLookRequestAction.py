import sys

from pydofus2.com.ankamagames.dofus.misc.utils.AbstractAction import \
    AbstractAction
from pydofus2.com.ankamagames.jerakine.handlers.messages.Action import Action


class JobCrafterContactLookRequestAction(AbstractAction, Action):

    crafterId: float

    def __init__(self, params: list = None):
        super().__init__(params)

    @classmethod
    def create(cls, crafterId: float) -> "JobCrafterContactLookRequestAction":
        act: JobCrafterContactLookRequestAction = cls(sys.argv[1:])
        act.crafterId = crafterId
        return act
