import math

from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import \
    IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import \
    ItemCriterion
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import \
    PlayerManager
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter
from pydofus2.com.ankamagames.jerakine.utils.pattern.PatternDecoder import \
    PatternDecoder


class SubscriptionDurationItemCriterion(ItemCriterion, IDataCenter):
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def text(self) -> str:
        readableCriterionValue = PatternDecoder.combine(
            I18n.getUiText("ui.social.daysSinceLastConnection", [self._criterionValue]),
            "n",
            self._criterionValue <= 1,
            self._criterionValue == 0,
        )
        readableCriterionRef = I18n.getUiText("ui.veteran.totalSubscriptionDuration")
        return readableCriterionRef + " " + self._operator.text + " " + readableCriterionValue

    def clone(self) -> IItemCriterion:
        return SubscriptionDurationItemCriterion(self.basicText)

    def getCriterion(self) -> int:
        return math.floor(PlayerManager().subscriptionDurationElapsed / (24 * 60 * 60))
