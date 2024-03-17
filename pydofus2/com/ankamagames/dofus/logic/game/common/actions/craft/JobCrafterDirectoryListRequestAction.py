import sys

from pydofus2.com.ankamagames.dofus.misc.utils.AbstractAction import \
    AbstractAction
from pydofus2.com.ankamagames.jerakine.handlers.messages.Action import Action


class JobCrafterDirectoryListRequestAction(AbstractAction, Action):

    jobId: int

    def __init__(self, params: list = None):
        super().__init__(params)

    @classmethod
    def create(cls, jobId: int) -> "JobCrafterDirectoryListRequestAction":
        act: JobCrafterDirectoryListRequestAction = cls(sys.argv[1:])
        act.jobId = jobId
        return act
