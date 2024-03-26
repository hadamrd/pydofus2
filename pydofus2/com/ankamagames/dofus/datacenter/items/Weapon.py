from pydofus2.com.ankamagames.dofus.datacenter.items.Item import Item
from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter


class Weapon(Item, IDataCenter):

    apCost: int

    minRange: int

    range: int

    maxCastPerTurn: int

    castInLine: bool

    castInDiagonal: bool

    castTestLos: bool

    criticalHitProbability: int

    criticalHitBonus: int

    criticalFailureProbability: int

    def __init__(self):
        self.apCost: int = None
        self.minRange: int = None
        self.range: int = None
        self.maxCastPerTurn: int = None
        self.castInLine: bool = None
        self.castInDiagonal: bool = None
        self.castTestLos: bool = None
        self.criticalHitProbability: int = None
        self.criticalHitBonus: int = None
        self.criticalFailureProbability: int = None
        super().__init__()

    @classmethod
    def getWeaponById(cls, weaponId: int) -> "Weapon":
        item: Item = Item.getItemById(weaponId)
        if item and item.isWeapon:
            return item
        return None

    @classmethod
    def getWeapons(self) -> list["Weapon"]:
        items = Item.getItems()
        result = list()
        for item in items:
            if item.isWeapon:
                result.append(item)
        return result

    idAccessors = IdAccessors(getWeaponById, getWeapons)

    @property
    def isWeapon(self) -> bool:
        return True

    @classmethod
    def copy(cls, src: Item, to: Item) -> None:
        super().copy(src, to)
        if hasattr(to, "apCost") and hasattr(src, "apCost"):
            to.apCost = src.apCost
            to.minRange = src.minRange
            to.range = src.range
            to.maxCastPerTurn = src.maxCastPerTurn
            to.castInLine = src.castInLine
            to.castInDiagonal = src.castInDiagonal
            to.castTestLos = src.castTestLos
            to.criticalHitProbability = src.criticalHitProbability
            to.criticalHitBonus = src.criticalHitBonus
            to.criticalFailureProbability = src.criticalFailureProbability
