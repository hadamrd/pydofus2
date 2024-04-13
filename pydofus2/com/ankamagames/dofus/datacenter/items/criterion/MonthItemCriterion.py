from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.TimeManager import TimeManager
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class MonthItemCriterion(ItemCriterion, IDataCenter):
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def text(self) -> str:
        readableCriterionValue: str = Month.getMonthById(self._criterionValue).name
        readableCriterionRef: str = I18n.getUiText("ui.time.months")
        return readableCriterionRef + " " + self._operator.text + " " + readableCriterionValue

    def clone(self) -> IItemCriterion:
        return MonthItemCriterion(self.basicText)

    def getCriterion(self) -> int:
        date: Date = Date()
        monthInt: int = TimeManager().getDateFromTime(date.getTime())[3]
        return monthInt - 1
