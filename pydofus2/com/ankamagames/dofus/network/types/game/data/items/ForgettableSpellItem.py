from pydofus2.com.ankamagames.dofus.network.types.game.data.items.SpellItem import SpellItem


class ForgettableSpellItem(SpellItem):
    available: bool

    def init(self, available_: bool, spellId_: int, spellLevel_: int):
        self.available = available_

        super().init(spellId_, spellLevel_)
