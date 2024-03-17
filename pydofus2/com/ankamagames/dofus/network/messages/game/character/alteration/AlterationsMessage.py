from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.alteration.AlterationInfo import \
        AlterationInfo
    

class AlterationsMessage(NetworkMessage):
    alterations: list['AlterationInfo']
    def init(self, alterations_: list['AlterationInfo']):
        self.alterations = alterations_
        
        super().__init__()
    