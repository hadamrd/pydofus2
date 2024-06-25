from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterionOperator import ItemCriterionOperator
from pydofus2.com.ankamagames.dofus.datacenter.quest.QuestObjective import QuestObjective
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger


class QuestObjectiveItemCriterion(ItemCriterion, IDataCenter):

    _objId: int

    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)
        self._objId = self._criterionValue

    @property
    def text(self) -> str:
        operator = self._operator.text
        s = self._serverCriterionForm[0:2]
        if s == "Qo":
            if operator == ItemCriterionOperator.EQUAL:
                return f"Quest objective '{self._objId}' must active"
            elif operator == ItemCriterionOperator.DIFFERENT:
                return f"Quest objective '{self._objId}' must not be an active"
            elif operator == ItemCriterionOperator.INFERIOR:
                return f"Quest objective '{self._objId}' must not be completed"
            elif operator == ItemCriterionOperator.SUPERIOR:
                return f"Quest objective '{self._objId}' must be completed"
            else:
                return "Unknown condition for the quest objective."

    @property
    def isRespected(self) -> bool:
        obj = QuestObjective.getQuestObjectiveById(self._objId)
        if not obj:
            Logger().warn(f"Unknown quest objective {self._objId}")
            return False
        questFrame = Kernel().questFrame
        activeObjs = questFrame.getActiveObjectives()
        completedObjs = questFrame.getCompletedObjectives()
        s = self._serverCriterionForm[0:2]
        if s == "Qo":
            if self._operator.text == ItemCriterionOperator.EQUAL:
                return self._objId in activeObjs
            if self._operator.text == ItemCriterionOperator.DIFFERENT:
                return self._objId not in activeObjs
            if self._operator.text == ItemCriterionOperator.INFERIOR:
                return self._objId not in completedObjs
            if self._operator.text == ItemCriterionOperator.SUPERIOR:
                return self._objId in completedObjs
        return False

    def clone(self) -> IItemCriterion:
        return QuestObjectiveItemCriterion(self.basicText)
