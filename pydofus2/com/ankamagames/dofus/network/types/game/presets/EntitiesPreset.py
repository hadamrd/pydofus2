from pydofus2.com.ankamagames.dofus.network.types.game.presets.Preset import Preset


class EntitiesPreset(Preset):
    iconId: int
    entityIds: list[int]

    def init(self, iconId_: int, entityIds_: list[int], id_: int):
        self.iconId = iconId_
        self.entityIds = entityIds_

        super().init(id_)
