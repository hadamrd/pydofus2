from pydofus2.com.ankamagames.dofus.network.types.game.shortcut.Shortcut import Shortcut


class ShortcutSmiley(Shortcut):
    smileyId: int

    def init(self, smileyId_: int, slot_: int):
        self.smileyId = smileyId_

        super().init(slot_)
