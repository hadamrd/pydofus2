from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.types.game.presets.Preset import \
    Preset

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.presets.CharacterCharacteristicForPreset import \
        CharacterCharacteristicForPreset
    

class FullStatsPreset(Preset):
    stats: list['CharacterCharacteristicForPreset']
    def init(self, stats_: list['CharacterCharacteristicForPreset'], id_: int):
        self.stats = stats_
        
        super().init(id_)
    