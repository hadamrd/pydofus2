from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.presets.Preset import \
        Preset
    

class PresetsContainerPreset(NetworkMessage):
    presets: list['Preset']
    def init(self, presets_: list['Preset']):
        self.presets = presets_
        
        super().__init__()
    