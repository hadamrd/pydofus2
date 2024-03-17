from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.IdentifiedEntityDispositionInformations import \
        IdentifiedEntityDispositionInformations
    

class GameEntitiesDispositionMessage(NetworkMessage):
    dispositions: list['IdentifiedEntityDispositionInformations']
    def init(self, dispositions_: list['IdentifiedEntityDispositionInformations']):
        self.dispositions = dispositions_
        
        super().__init__()
    