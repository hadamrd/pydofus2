from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.messages.game.atlas.compass.CompassUpdateMessage import \
    CompassUpdateMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.MapCoordinates import \
        MapCoordinates
    

class CompassUpdatePartyMemberMessage(CompassUpdateMessage):
    memberId: int
    active: bool
    def init(self, memberId_: int, active_: bool, type_: int, coords_: 'MapCoordinates'):
        self.memberId = memberId_
        self.active = active_
        
        super().init(type_, coords_)
    