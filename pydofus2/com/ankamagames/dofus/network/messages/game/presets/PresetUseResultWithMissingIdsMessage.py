from pydofus2.com.ankamagames.dofus.network.messages.game.presets.PresetUseResultMessage import PresetUseResultMessage


class PresetUseResultWithMissingIdsMessage(PresetUseResultMessage):
    missingIds: list[int]

    def init(self, missingIds_: list[int], presetId_: int, code_: int):
        self.missingIds = missingIds_

        super().init(presetId_, code_)
