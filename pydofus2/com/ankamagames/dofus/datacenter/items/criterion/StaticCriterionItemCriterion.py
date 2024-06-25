from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion


class StaticCriterionItemCriterion(ItemCriterion):
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def text(self) -> str:
        return ""

    @property
    def isRespected(self) -> bool:
        return True

    def clone(self) -> IItemCriterion:
        return StaticCriterionItemCriterion(self.basicText)

    def getCriterion(self) -> int:
        return 0
