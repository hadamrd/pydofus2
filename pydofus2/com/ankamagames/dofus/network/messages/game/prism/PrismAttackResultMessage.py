from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.prism.PrismGeolocalizedInformation import \
        PrismGeolocalizedInformation
    

class PrismAttackResultMessage(NetworkMessage):
    prism: 'PrismGeolocalizedInformation'
    result: int
    def init(self, prism_: 'PrismGeolocalizedInformation', result_: int):
        self.prism = prism_
        self.result = result_
        
        super().__init__()
    