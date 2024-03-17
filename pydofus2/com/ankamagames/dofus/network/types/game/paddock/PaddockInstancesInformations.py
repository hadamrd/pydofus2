from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.paddock.PaddockInformations import \
    PaddockInformations

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.paddock.PaddockBuyableInformations import \
        PaddockBuyableInformations
    

class PaddockInstancesInformations(PaddockInformations):
    paddocks: list['PaddockBuyableInformations']
    def init(self, paddocks_: list['PaddockBuyableInformations'], maxOutdoorMount_: int, maxItems_: int):
        self.paddocks = paddocks_
        
        super().init(maxOutdoorMount_, maxItems_)
    