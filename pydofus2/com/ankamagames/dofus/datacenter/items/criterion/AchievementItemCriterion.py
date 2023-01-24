from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import (
    IItemCriterion,
)
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class AchievementItemCriterion(ItemCriterion, IDataCenter):
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def isRespected(self) -> bool:
        id: int = 0
        achievementFinishedList: list = Kernel().worker.getFrame("QuestFrame")
        for id in achievementFinishedList:
            if id == self._criterionValue:
                return True
        return False

    def clone(self) -> IItemCriterion:
        return AchievementItemCriterion(self.basicText)

    def getCriterion(self) -> int:
        id: int = 0
        achievementFinishedList: list = Kernel().worker.getFrame("QuestFrame")
        for id in achievementFinishedList:
            if id == self._criterionValue:
                return 1
        return 0
