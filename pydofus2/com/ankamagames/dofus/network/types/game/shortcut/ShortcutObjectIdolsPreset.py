from pydofus2.com.ankamagames.dofus.network.types.game.shortcut.ShortcutObject import ShortcutObject


class ShortcutObjectIdolsPreset(ShortcutObject):
    presetId: int

    def init(self, presetId_: int, slot_: int):
        self.presetId = presetId_

        super().init(slot_)
