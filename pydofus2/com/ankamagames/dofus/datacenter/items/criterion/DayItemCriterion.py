from datetime import datetime

from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import \
    IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import \
    ItemCriterion
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.TimeManager import \
    TimeManager
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter
from pydofus2.com.ankamagames.jerakine.utils.pattern.PatternDecoder import \
    PatternDecoder


class DayItemCriterion(ItemCriterion, IDataCenter):
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def text(self) -> str:
        readableCriterionValue: str = str(self._criterionValue)
        readableCriterionRef: str = PatternDecoder.combine(I18n.getUiText("ui.time.days"), "n", True)
        return readableCriterionRef + " " + self._operator.text + " " + readableCriterionValue

    def clone(self) -> "IItemCriterion":
        return DayItemCriterion(self.basicText)

    def getCriterion(self) -> int:
        date = datetime.now()
        return TimeManager().getDateFromTime(int(date.timestamp()))[2]
