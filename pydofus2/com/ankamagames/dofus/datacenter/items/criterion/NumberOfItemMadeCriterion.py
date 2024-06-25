from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class NumberOfItemMadeCriterion(ItemCriterion, IDataCenter):
    def __init__(pCriterion: str):
        super().__init__(pCriterion)

    @property
    def text(self) -> str:
        readableCriterionValue: str = self._criterionValueText
        itemsMadeCount: int = int(readableCriterionValue.split(",")[1]) + 1
        return I18n.getUiText("ui.smithmagic.itemsMadeCount", [itemsMadeCount])

    def clone(self) -> IItemCriterion:
        return NumberOfItemMadeCriterion(self.basicText)
