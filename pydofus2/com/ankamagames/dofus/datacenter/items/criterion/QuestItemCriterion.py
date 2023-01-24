from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.quest.Quest import Quest
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.common.frames.QuestFrame import QuestFrame
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.quest.QuestActiveInformations import (
    QuestActiveInformations,
)
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class QuestItemCriterion(ItemCriterion, IDataCenter):

    _questId: int

    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)
        self._questId = self._criterionValue

    @property
    def text(self) -> str:
        readableCriterion: str = ""
        quest: Quest = Quest.getQuestById(self._questId)
        if not quest:
            return readableCriterion
        readableCriterionValue: str = quest.name
        s: str = self._serverCriterionForm.slice(0, 2)
        if s == "Qa":
            readableCriterion = I18n.getUiText("ui.grimoire.quest.active", [readableCriterionValue])

        elif s == "Qc":
            readableCriterion = I18n.getUiText("ui.grimoire.quest.startable", [readableCriterionValue])

        elif s == "Qf":
            readableCriterion = I18n.getUiText("ui.grimoire.quest.done", [readableCriterionValue])
        return readableCriterion

    @property
    def isRespected(self) -> bool:
        questFrame: QuestFrame = None
        completedQuests: list[int] = None
        questA: QuestActiveInformations = None
        quest: Quest = Quest.getQuestById(self._questId)
        if not quest:
            return False
        questFrame = Kernel().worker.getFrame("QuestFrame")
        s: str = self._serverCriterionForm[0:2]
        if s == "Qa":
            for questA in questFrame.getActiveQuests():
                if questA.questId == self._questId:
                    return True
        elif s == "Qc":
            return True
        elif s == "Qf":
            completedQuests = questFrame.getCompletedQuests()
            return self._questId in completedQuests if completedQuests else False
        return False

    def clone(self) -> IItemCriterion:
        return QuestItemCriterion(self.basicText)

    def getCriterion(self) -> int:
        return PlayedCharacterManager().infos.level
