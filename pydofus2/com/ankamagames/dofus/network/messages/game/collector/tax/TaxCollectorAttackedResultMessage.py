from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.collector.tax.TaxCollectorBasicInformations import \
        TaxCollectorBasicInformations
    from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.BasicAllianceInformations import \
        BasicAllianceInformations
    

class TaxCollectorAttackedResultMessage(NetworkMessage):
    deadOrAlive: bool
    basicInfos: 'TaxCollectorBasicInformations'
    alliance: 'BasicAllianceInformations'
    def init(self, deadOrAlive_: bool, basicInfos_: 'TaxCollectorBasicInformations', alliance_: 'BasicAllianceInformations'):
        self.deadOrAlive = deadOrAlive_
        self.basicInfos = basicInfos_
        self.alliance = alliance_
        
        super().__init__()
    