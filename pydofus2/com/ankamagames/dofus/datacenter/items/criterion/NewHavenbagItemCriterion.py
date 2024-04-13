from pydofus2.com.ankamagames.dofus.datacenter.houses.HavenbagTheme import HavenbagTheme
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterionOperator import ItemCriterionOperator
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class NewHavenbagItemCriterion(ItemCriterion, IDataCenter):
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def text(self) -> str:
        readableCriterionRef: str = None
        havenbagTheme: str = HavenbagTheme.getTheme(self._criterionValue).name
        if self._operator.text == ItemCriterionOperator.DIFFERENT:
            readableCriterionRef = I18n.getUiText("ui.criterion.notHavenbagTheme", [havenbagTheme])
        else:
            readableCriterionRef = I18n.getUiText("ui.criterion.hasHavenbagTheme", [havenbagTheme])
        return readableCriterionRef

    def clone(self) -> IItemCriterion:
        return NewHavenbagItemCriterion(self.basicText)
