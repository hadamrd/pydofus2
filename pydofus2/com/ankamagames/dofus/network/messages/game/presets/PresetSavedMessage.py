from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.presets.Preset import \
        Preset
    

class PresetSavedMessage(NetworkMessage):
    presetId: int
    preset: 'Preset'
    def init(self, presetId_: int, preset_: 'Preset'):
        self.presetId = presetId_
        self.preset = preset_
        
        super().__init__()
    