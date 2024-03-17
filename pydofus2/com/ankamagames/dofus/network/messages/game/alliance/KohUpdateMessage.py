from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.alliance.KohAllianceInfo import \
        KohAllianceInfo
    

class KohUpdateMessage(NetworkMessage):
    kohAllianceInfo: list['KohAllianceInfo']
    startingAvaTimestamp: int
    nextTickTime: int
    def init(self, kohAllianceInfo_: list['KohAllianceInfo'], startingAvaTimestamp_: int, nextTickTime_: int):
        self.kohAllianceInfo = kohAllianceInfo_
        self.startingAvaTimestamp = startingAvaTimestamp_
        self.nextTickTime = nextTickTime_
        
        super().__init__()
    