from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.collector.tax.TaxCollectorOrderedSpell import \
        TaxCollectorOrderedSpell
    from pydofus2.com.ankamagames.dofus.network.types.game.uuid import Uuid


class TaxCollectorPresetSpellUpdatedMessage(NetworkMessage):
    presetId: "Uuid"
    taxCollectorSpells: list["TaxCollectorOrderedSpell"]

    def init(self, presetId_: "Uuid", taxCollectorSpells_: list["TaxCollectorOrderedSpell"]):
        self.presetId = presetId_
        self.taxCollectorSpells = taxCollectorSpells_

        super().__init__()
