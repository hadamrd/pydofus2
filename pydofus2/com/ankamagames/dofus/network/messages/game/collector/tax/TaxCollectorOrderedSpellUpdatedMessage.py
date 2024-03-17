from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.collector.tax.TaxCollectorOrderedSpell import \
        TaxCollectorOrderedSpell
    

class TaxCollectorOrderedSpellUpdatedMessage(NetworkMessage):
    taxCollectorId: int
    taxCollectorSpells: list['TaxCollectorOrderedSpell']
    def init(self, taxCollectorId_: int, taxCollectorSpells_: list['TaxCollectorOrderedSpell']):
        self.taxCollectorId = taxCollectorId_
        self.taxCollectorSpells = taxCollectorSpells_
        
        super().__init__()
    