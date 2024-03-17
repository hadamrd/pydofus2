from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.house.HouseInformationsForGuild import \
        HouseInformationsForGuild
    

class GuildHouseUpdateInformationMessage(NetworkMessage):
    housesInformations: 'HouseInformationsForGuild'
    def init(self, housesInformations_: 'HouseInformationsForGuild'):
        self.housesInformations = housesInformations_
        
        super().__init__()
    