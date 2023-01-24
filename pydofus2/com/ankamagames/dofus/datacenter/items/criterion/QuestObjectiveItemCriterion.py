from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import (
    IItemCriterion,
)
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterionOperator import (
    ItemCriterionOperator,
)
from pydofus2.com.ankamagames.dofus.datacenter.quest.QuestObjective import QuestObjective
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.logic.common.frames.QuestFrame import QuestFrame


class QuestObjectiveItemCriterion(ItemCriterion, IDataCenter):

    _objId: int

    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)
        self._objId = self._criterionValue

    @property
    def text(self) -> str:
        return ""

    @property
    def isRespected(self) -> bool:
        obj: QuestObjective = QuestObjective.getQuestObjectiveById(self._objId)
        if not obj:
            return False
        questFrame: "QuestFrame" = Kernel().worker.getFrame("QuestFrame")
        activeObjs: list[int] = questFrame.getActiveObjectives()
        completedObjs: list[int] = questFrame.getCompletedObjectives()
        s: str = self._serverCriterionForm[0:2]
        if s == "Qo":
            if self._operator.text == ItemCriterionOperator.EQUAL:
                return self._objId in activeObjs
            if self._operator.text == ItemCriterionOperator.DIFFERENT:
                return self._objId in activeObjs
            if self._operator.text == ItemCriterionOperator.INFERIOR:
                return self._objId in completedObjs
            if self._operator.text == ItemCriterionOperator.SUPERIOR:
                return self._objId in completedObjs
        return False

    def clone(self) -> IItemCriterion:
        return QuestObjectiveItemCriterion(self.basicText)
