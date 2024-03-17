from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.datacenter.spells.Spell import Spell


class SpellVariant(IDataCenter):
    MODULE: str = "SpellVariants"

    def __init__(self):
        super().__init__()
        self.id: int
        self.breedId: int
        self.spellIds = list[int]()
        self._spells = list["Spell"]()

    @classmethod
    def getSpellVariantById(cls, id: int) -> "SpellVariant":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getSpellVariants(cls) -> list["SpellVariant"]:
        return GameData().getObjects(cls.MODULE)

    @property
    def spells(self) -> list["Spell"]:
        from pydofus2.com.ankamagames.dofus.datacenter.spells.Spell import \
            Spell

        if not self._spells:
            for spellId in self.spellIds:
                spell = Spell.getSpellById(spellId)
                if spell:
                    self._spells.append(spell)
        return self._spells

    def __str__(self) -> str:
        result: str = ""
        result += "[Variante " + self.id + " : "
        name0: str = "???"
        name1: str = "???"
        id0: int = 0
        id1: int = 0
        if len(self.spells) and self.spells[0]:
            name0 = self.spells[0].name
        if len(self.spells) > 1 and self.spells[1]:
            name1 = self.spells[1].name
        if len(self.spellIds) and self.spellIds[0]:
            id0 = self.spellIds[0]
        if len(self.spellIds) > 1 and self.spellIds[1]:
            id1 = self.spellIds[1]
        return result + (name0 + " (" + id0 + ")" + ", " + name1 + " (" + id1 + ")]")
