from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.presets.Preset import Preset

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.presets.SpellForPreset import SpellForPreset
    from pydofus2.com.ankamagames.dofus.network.types.game.presets.SpellsPreset import SpellsPreset


class ForgettableSpellsPreset(Preset):
    baseSpellsPreset: "SpellsPreset"
    forgettableSpells: list["SpellForPreset"]

    def init(self, baseSpellsPreset_: "SpellsPreset", forgettableSpells_: list["SpellForPreset"], id_: int):
        self.baseSpellsPreset = baseSpellsPreset_
        self.forgettableSpells = forgettableSpells_

        super().init(id_)
