from com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from com.ankamagames.dofus.network.types.game.house.HouseInformationsForGuild import HouseInformationsForGuild
    


class GuildHousesInformationMessage(NetworkMessage):
    housesInformations:list['HouseInformationsForGuild']
    

    def init(self, housesInformations:list['HouseInformationsForGuild']):
        self.housesInformations = housesInformations
        
        super().__init__()
    
    