from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import \
    IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import \
    ItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterionOperator import \
    ItemCriterionOperator
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter


class AchievementItemCriterion(ItemCriterion, IDataCenter):
    
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def isRespected(self) -> bool:
        achievementFinishedList = Kernel().questFrame.finishedAccountAchievementIds
        for id in achievementFinishedList:
            if id == self._criterionValue:
                return True
        return False

    def clone(self) -> IItemCriterion:
        return AchievementItemCriterion(self.basicText)

    @property
    def text(self) -> str:
        from pydofus2.com.ankamagames.dofus.datacenter.quest.Achievement import \
            Achievement

        readableValue = f" '{Achievement.getAchievementById(self._criterionValue).name}'"
        readableCriterion = I18n.getUiText("ui.tooltip.unlockAchievement", [readableValue])
        
        if self._operator.text == ItemCriterionOperator.DIFFERENT:
            readableCriterion = I18n.getUiText("ui.tooltip.dontUnlockAchievement", [readableValue])

        return readableCriterion
    
    def getCriterion(self) -> int:
        achievementFinishedList = Kernel().questFrame.finishedAccountAchievementIds
        for id in achievementFinishedList:
            if id == self._criterionValue:
                return 1
        return 0
