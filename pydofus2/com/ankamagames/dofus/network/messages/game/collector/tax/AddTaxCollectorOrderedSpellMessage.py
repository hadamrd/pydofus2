from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.collector.tax.TaxCollectorOrderedSpell import \
        TaxCollectorOrderedSpell


class AddTaxCollectorOrderedSpellMessage(NetworkMessage):
    taxCollectorId: int
    spell: "TaxCollectorOrderedSpell"

    def init(self, taxCollectorId_: int, spell_: "TaxCollectorOrderedSpell"):
        self.taxCollectorId = taxCollectorId_
        self.spell = spell_

        super().__init__()
