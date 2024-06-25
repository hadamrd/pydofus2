from typing import TYPE_CHECKING

import pydofus2.com.ankamagames.dofus.datacenter.quest.QuestCategory as qstcat
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.GroupItemCriterion import GroupItemCriterion
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.network.types.game.context.roleplay.quest.GameRolePlayNpcQuestFlag import (
    GameRolePlayNpcQuestFlag,
)
from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.datacenter.quest.QuestStep import QuestStep


class Quest(IDataCenter):

    MODULE: str = "Quests"

    id: int

    nameId: int

    stepIds: list[int]

    categoryId: int

    repeatType: int

    repeatLimit: int

    isDungeonQuest: bool

    levelMin: int

    levelMax: int

    isPartyQuest: bool

    startCriterion: str

    followable: bool

    _name: str = None

    _steps: list["QuestStep"] = None

    _conditions: GroupItemCriterion = None

    def __init__(self):
        super().__init__()

    def getFirstValidQuest(self, questFlag: GameRolePlayNpcQuestFlag) -> "Quest":
        validQuest: Quest = None
        quest: Quest = None
        questId: int = 0
        res1: int = 0
        res2: int = 0
        validQuestRes: int = 0
        for questId in questFlag.questsToValidId:
            quest = Quest.getQuestById(questId)
            if quest != None:
                res1 = quest.getPriorityValue()
                if validQuestRes < res1 or validQuest == None:
                    validQuest = quest
                    validQuestRes = res1
        for questId in questFlag.questsToStartId:
            quest = Quest.getQuestById(questId)
            if quest != None:
                res2 = quest.getPriorityValue()
                if validQuestRes < res2 or validQuest == None:
                    validQuest = quest
                    validQuestRes = res2
        return validQuest

    @classmethod
    def getQuestById(cls, id: int) -> "Quest":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getQuests(cls) -> list["Quest"]:
        return GameData().getObjects(cls.MODULE)

    @property
    def name(self) -> str:
        if not self._name:
            self._name = I18n.getText(self.nameId)
        return self._name

    @property
    def steps(self) -> list["QuestStep"]:
        from pydofus2.com.ankamagames.dofus.datacenter.quest.QuestStep import QuestStep

        if not self._steps:
            self._steps = [QuestStep.getQuestStepById(s) for s in self.stepIds]
        return self._steps

    @property
    def category(self) -> qstcat.QuestCategory:
        return qstcat.QuestCategory.getQuestCategoryById(self.categoryId)

    @property
    def canBeStarted(self) -> bool:
        if not self._conditions and self.startCriterion:
            self._conditions = GroupItemCriterion(self.startCriterion)
        return bool(self._conditions.isRespected) if self._conditions else True

    def getPriorityValue(self) -> int:
        playerLvl: int = PlayedCharacterManager().limitedLevel
        res: int = 0
        if playerLvl >= self.levelMin and playerLvl <= self.levelMax:
            res += 10000
        if self.repeatType != 0:
            res += 1000
        return res

    idAccessors: IdAccessors = IdAccessors(getQuestById, getQuests)
