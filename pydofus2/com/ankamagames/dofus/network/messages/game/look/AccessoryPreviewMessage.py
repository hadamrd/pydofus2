from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.look.EntityLook import \
        EntityLook
    

class AccessoryPreviewMessage(NetworkMessage):
    look: 'EntityLook'
    def init(self, look_: 'EntityLook'):
        self.look = look_
        
        super().__init__()
    