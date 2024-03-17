from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.job.JobDescription import \
        JobDescription
    

class JobDescriptionMessage(NetworkMessage):
    jobsDescription: list['JobDescription']
    def init(self, jobsDescription_: list['JobDescription']):
        self.jobsDescription = jobsDescription_
        
        super().__init__()
    