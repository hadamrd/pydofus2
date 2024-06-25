import sys

from pydofus2.com.ankamagames.dofus.misc.utils.AbstractAction import AbstractAction
from pydofus2.com.ankamagames.jerakine.handlers.messages.Action import Action


class JobBookSubscribeRequestAction(AbstractAction, Action):

    jobIds: list[int]

    def __init__(self, params: list = None):
        super().__init__(params)

    @classmethod
    def create(cls, jobIds: list[int]) -> "JobBookSubscribeRequestAction":
        action: JobBookSubscribeRequestAction = cls(sys.argv[1:])
        action.jobIds = jobIds
        return action
