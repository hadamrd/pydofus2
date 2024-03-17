from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.job.JobCrafterDirectoryListEntry import \
        JobCrafterDirectoryListEntry
    

class JobCrafterDirectoryAddMessage(NetworkMessage):
    listEntry: 'JobCrafterDirectoryListEntry'
    def init(self, listEntry_: 'JobCrafterDirectoryListEntry'):
        self.listEntry = listEntry_
        
        super().__init__()
    