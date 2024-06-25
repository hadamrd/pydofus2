from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class AchievementPioneerItemCriterion(ItemCriterion, IDataCenter):

    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    def clone(self) -> "AchievementPioneerItemCriterion":
        return AchievementPioneerItemCriterion(self.basicText)

    @property
    def text(self) -> str:
        return ""

    @property
    def is_respected(self) -> bool:
        achievementId, criterionValue = map(int, self._criterionValueText.split(","))
        questFrame = Kernel().questFrame
        if achievementId in questFrame.finishedCharacterAchievementByIds:
            pioneerRank = int(questFrame.finishedCharacterAchievementByIds[achievementId].achievedPioneerRank)
        else:
            pioneerRank = int(questFrame.achievementPioneerRanks.get(achievementId, 1))
        return self._operator.compare(pioneerRank, criterionValue)
