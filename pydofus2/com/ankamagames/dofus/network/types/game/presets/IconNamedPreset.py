from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.presets.PresetsContainerPreset import PresetsContainerPreset

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.presets.Preset import Preset


class IconNamedPreset(PresetsContainerPreset):
    iconId: int
    name: str

    def init(self, iconId_: int, name_: str, presets_: list["Preset"]):
        self.iconId = iconId_
        self.name = name_

        super().init(presets_)
