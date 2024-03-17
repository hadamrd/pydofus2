from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightCharacteristics import \
        GameFightCharacteristics
    

class RefreshCharacterStatsMessage(NetworkMessage):
    fighterId: int
    stats: 'GameFightCharacteristics'
    def init(self, fighterId_: int, stats_: 'GameFightCharacteristics'):
        self.fighterId = fighterId_
        self.stats = stats_
        
        super().__init__()
    