from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.job.JobCrafterDirectorySettings import \
        JobCrafterDirectorySettings
    

class JobCrafterDirectorySettingsMessage(NetworkMessage):
    craftersSettings: list['JobCrafterDirectorySettings']
    def init(self, craftersSettings_: list['JobCrafterDirectorySettings']):
        self.craftersSettings = craftersSettings_
        
        super().__init__()
    