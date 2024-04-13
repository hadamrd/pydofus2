from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.collector.tax.TaxCollectorOrderedSpell import (
        TaxCollectorOrderedSpell,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.uuid import Uuid


class AddTaxCollectorPresetSpellMessage(NetworkMessage):
    presetId: "Uuid"
    spell: "TaxCollectorOrderedSpell"

    def init(self, presetId_: "Uuid", spell_: "TaxCollectorOrderedSpell"):
        self.presetId = presetId_
        self.spell = spell_

        super().__init__()
