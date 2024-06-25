from pydofus2.com.ankamagames.dofus.network.messages.game.presets.IconPresetSaveRequestMessage import (
    IconPresetSaveRequestMessage,
)


class IdolsPresetSaveRequestMessage(IconPresetSaveRequestMessage):
    def init(self, presetId_: int, symbolId_: int, updateData_: bool):

        super().init(presetId_, symbolId_, updateData_)
