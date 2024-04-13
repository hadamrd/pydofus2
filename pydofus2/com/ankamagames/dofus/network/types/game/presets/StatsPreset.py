from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.presets.Preset import Preset

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.presets.SimpleCharacterCharacteristicForPreset import (
        SimpleCharacterCharacteristicForPreset,
    )


class StatsPreset(Preset):
    stats: list["SimpleCharacterCharacteristicForPreset"]

    def init(self, stats_: list["SimpleCharacterCharacteristicForPreset"], id_: int):
        self.stats = stats_

        super().init(id_)
