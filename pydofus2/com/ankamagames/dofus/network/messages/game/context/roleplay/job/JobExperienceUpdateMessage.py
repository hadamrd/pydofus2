from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.job.JobExperience import \
        JobExperience


class JobExperienceUpdateMessage(NetworkMessage):
    experiencesUpdate: "JobExperience"

    def init(self, experiencesUpdate_: "JobExperience"):
        self.experiencesUpdate = experiencesUpdate_

        super().__init__()
