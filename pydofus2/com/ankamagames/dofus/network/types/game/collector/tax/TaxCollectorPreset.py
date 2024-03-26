from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.characteristic.CharacterCharacteristics import \
        CharacterCharacteristics
    from pydofus2.com.ankamagames.dofus.network.types.game.collector.tax.TaxCollectorOrderedSpell import \
        TaxCollectorOrderedSpell
    from pydofus2.com.ankamagames.dofus.network.types.game.uuid import Uuid


class TaxCollectorPreset(NetworkMessage):
    presetId: "Uuid"
    spells: list["TaxCollectorOrderedSpell"]
    characteristics: "CharacterCharacteristics"

    def init(
        self,
        presetId_: "Uuid",
        spells_: list["TaxCollectorOrderedSpell"],
        characteristics_: "CharacterCharacteristics",
    ):
        self.presetId = presetId_
        self.spells = spells_
        self.characteristics = characteristics_

        super().__init__()
