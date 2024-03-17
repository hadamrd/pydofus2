from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.Uuid import Uuid
    

class RemoveTaxCollectorPresetSpellMessage(NetworkMessage):
    presetId: 'Uuid'
    slot: int
    def init(self, presetId_: 'Uuid', slot_: int):
        self.presetId = presetId_
        self.slot = slot_
        
        super().__init__()
    