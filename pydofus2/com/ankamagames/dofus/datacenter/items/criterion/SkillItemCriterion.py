from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class SkillItemCriterion(ItemCriterion, IDataCenter):
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def text(self) -> str:
        return self._criterionRef + " " + self._operator.text + " " + self._criterionValue

    def clone(self) -> IItemCriterion:
        return SkillItemCriterion(self.basicText)

    def getCriterion(self) -> int:
        return 0
