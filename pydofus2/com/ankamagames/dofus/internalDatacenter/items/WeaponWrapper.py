from pydofus2.com.ankamagames.dofus.datacenter.items.Weapon import Weapon
from pydofus2.com.ankamagames.dofus.internalDatacenter.items.ItemWrapper import ItemWrapper


class WeaponWrapper(ItemWrapper):

    _weaponUtil: Weapon = Weapon()

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
        super().__init__()

    @property
    def isWeapon(self) -> bool:
        return True

    def clone(self, baseobject: object = None) -> ItemWrapper:
        result: ItemWrapper = super().clone(baseobject)
        self._weaponUtil.copy(self, result)
        return result
