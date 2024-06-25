from pydofus2.com.ankamagames.dofus.datacenter.items.Item import Item
from pydofus2.com.ankamagames.dofus.datacenter.spells.SpellPair import SpellPair
from pydofus2.com.ankamagames.dofus.misc.utils.GameDataQuery import GameDataQuery
from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class Idol(IDataCenter):

    MODULE: str = "Idols"

    _item: Item = None

    _spellPair: SpellPair

    _name: str = None

    id: int

    description: str

    categoryId: int

    itemId: int

    groupOnly: bool

    spellPairId: int

    score: int

    experienceBonus: int

    dropBonus: int

    synergyIdolsIds: list[int]

    synergyIdolsCoeff: list[float]

    incompatibleMonsters: list[int]

    def __init__(self):
        super().__init__()

    def getIdolByItemId(self, id: int) -> "Idol":
        idolsIds: list[int] = GameDataQuery.queryEquals(Idol, "itemId", id)
        return self.getIdolById(idolsIds[0]) if idolsIds and len(idolsIds) > 0 else None

    @classmethod
    def getIdolById(cls, id: int) -> "Idol":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getIdols(cls) -> list["Idol"]:
        return GameData().getObjects(cls.MODULE)

    @property
    def item(self) -> Item:
        if not self._item:
            self._item = Item.getItemById(self.itemId)
        return self._item

    @property
    def name(self) -> str:
        if not self._name:
            self._name = self.item.name
        return self._name

    @property
    def spellPair(self) -> SpellPair:
        if not self._spellPair:
            self._spellPair = SpellPair.getSpellPairById(self.spellPairId)
        return self._spellPair

    idAccessors: IdAccessors = IdAccessors(getIdolById, getIdols)
