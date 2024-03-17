from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.EntityMovementInformations import \
        EntityMovementInformations
    

class GameContextMoveElementMessage(NetworkMessage):
    movement: 'EntityMovementInformations'
    def init(self, movement_: 'EntityMovementInformations'):
        self.movement = movement_
        
        super().__init__()
    