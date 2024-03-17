from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.data.items.effects.ObjectEffect import \
        ObjectEffect
    

class AlterationInfo(NetworkMessage):
    alterationId: int
    creationTime: int
    expirationType: int
    expirationValue: int
    effects: list['ObjectEffect']
    def init(self, alterationId_: int, creationTime_: int, expirationType_: int, expirationValue_: int, effects_: list['ObjectEffect']):
        self.alterationId = alterationId_
        self.creationTime = creationTime_
        self.expirationType = expirationType_
        self.expirationValue = expirationValue_
        self.effects = effects_
        
        super().__init__()
    