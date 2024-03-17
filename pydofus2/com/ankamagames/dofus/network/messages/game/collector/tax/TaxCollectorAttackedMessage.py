from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.BasicAllianceInformations import \
        BasicAllianceInformations
    

class TaxCollectorAttackedMessage(NetworkMessage):
    firstNameId: int
    lastNameId: int
    worldX: int
    worldY: int
    mapId: int
    subAreaId: int
    alliance: 'BasicAllianceInformations'
    def init(self, firstNameId_: int, lastNameId_: int, worldX_: int, worldY_: int, mapId_: int, subAreaId_: int, alliance_: 'BasicAllianceInformations'):
        self.firstNameId = firstNameId_
        self.lastNameId = lastNameId_
        self.worldX = worldX_
        self.worldY = worldY_
        self.mapId = mapId_
        self.subAreaId = subAreaId_
        self.alliance = alliance_
        
        super().__init__()
    