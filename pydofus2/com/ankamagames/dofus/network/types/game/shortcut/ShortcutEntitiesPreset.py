from pydofus2.com.ankamagames.dofus.network.types.game.shortcut.Shortcut import Shortcut


class ShortcutEntitiesPreset(Shortcut):
    presetId: int

    def init(self, presetId_: int, slot_: int):
        self.presetId = presetId_

        super().init(slot_)
