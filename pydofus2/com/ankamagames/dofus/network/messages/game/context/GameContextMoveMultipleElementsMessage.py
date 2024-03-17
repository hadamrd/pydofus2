from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.EntityMovementInformations import \
        EntityMovementInformations
    

class GameContextMoveMultipleElementsMessage(NetworkMessage):
    movements: list['EntityMovementInformations']
    def init(self, movements_: list['EntityMovementInformations']):
        self.movements = movements_
        
        super().__init__()
    