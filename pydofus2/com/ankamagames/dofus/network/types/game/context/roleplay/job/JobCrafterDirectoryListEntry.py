from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.job.JobCrafterDirectoryEntryJobInfo import (
        JobCrafterDirectoryEntryJobInfo,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.job.JobCrafterDirectoryEntryPlayerInfo import (
        JobCrafterDirectoryEntryPlayerInfo,
    )


class JobCrafterDirectoryListEntry(NetworkMessage):
    playerInfo: "JobCrafterDirectoryEntryPlayerInfo"
    jobInfo: "JobCrafterDirectoryEntryJobInfo"

    def init(self, playerInfo_: "JobCrafterDirectoryEntryPlayerInfo", jobInfo_: "JobCrafterDirectoryEntryJobInfo"):
        self.playerInfo = playerInfo_
        self.jobInfo = jobInfo_

        super().__init__()
