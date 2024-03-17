from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.friend.AcquaintanceInformation import \
        AcquaintanceInformation
    

class AcquaintanceAddedMessage(NetworkMessage):
    acquaintanceAdded: 'AcquaintanceInformation'
    def init(self, acquaintanceAdded_: 'AcquaintanceInformation'):
        self.acquaintanceAdded = acquaintanceAdded_
        
        super().__init__()
    