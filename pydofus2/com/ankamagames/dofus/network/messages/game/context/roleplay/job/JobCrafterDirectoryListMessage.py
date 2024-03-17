from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.job.JobCrafterDirectoryListEntry import \
        JobCrafterDirectoryListEntry
    

class JobCrafterDirectoryListMessage(NetworkMessage):
    listEntries: list['JobCrafterDirectoryListEntry']
    def init(self, listEntries_: list['JobCrafterDirectoryListEntry']):
        self.listEntries = listEntries_
        
        super().__init__()
    