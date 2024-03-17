from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.prism.PrismInformation import \
        PrismInformation
    

class PrismGeolocalizedInformation(NetworkMessage):
    subAreaId: int
    allianceId: int
    worldX: int
    worldY: int
    mapId: int
    prism: 'PrismInformation'
    def init(self, subAreaId_: int, allianceId_: int, worldX_: int, worldY_: int, mapId_: int, prism_: 'PrismInformation'):
        self.subAreaId = subAreaId_
        self.allianceId = allianceId_
        self.worldX = worldX_
        self.worldY = worldY_
        self.mapId = mapId_
        self.prism = prism_
        
        super().__init__()
    