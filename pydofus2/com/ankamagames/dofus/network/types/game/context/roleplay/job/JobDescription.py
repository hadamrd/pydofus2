from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.interactive.skill.SkillActionDescription import \
        SkillActionDescription
    

class JobDescription(NetworkMessage):
    jobId: int
    skills: list['SkillActionDescription']
    def init(self, jobId_: int, skills_: list['SkillActionDescription']):
        self.jobId = jobId_
        self.skills = skills_
        
        super().__init__()
    