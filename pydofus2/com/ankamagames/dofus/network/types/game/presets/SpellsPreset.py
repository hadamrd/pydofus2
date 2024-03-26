from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.presets.Preset import \
    Preset

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.presets.SpellForPreset import \
        SpellForPreset


class SpellsPreset(Preset):
    spells: list["SpellForPreset"]

    def init(self, spells_: list["SpellForPreset"], id_: int):
        self.spells = spells_

        super().init(id_)
