from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.datacenter.quest.NpcMessage import NpcMessage
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.datacenter.quest.QuestObjective import QuestObjective
    from pydofus2.com.ankamagames.dofus.datacenter.quest.QuestStepRewards import QuestStepRewards


class QuestStep(IDataCenter):

    MODULE: str = "QuestSteps"

    id: int

    questId: int

    nameId: int

    descriptionId: int

    dialogId: int

    optimalLevel: int

    duration: float

    _currentLevelRewards: "QuestStepRewards" = None

    objectiveIds: list[int]

    rewardsIds: list[int]

    _name: str = None

    _description: str = None

    _dialog: str = None

    _objectives: list["QuestObjective"] = None

    def __init__(self):
        super().__init__()

    @classmethod
    def getQuestStepById(cls, id: int) -> "QuestStep":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getQuestSteps(cls) -> list["QuestStep"]:
        return GameData().getObjects(cls.MODULE)

    @property
    def kamasReward(self) -> float:
        self.initCurrentLevelRewards()
        return float(0) if self._currentLevelRewards == None else float(self._currentLevelRewards.kamasReward)

    @property
    def experienceReward(self) -> int:
        self.initCurrentLevelRewards()
        return int(0) if self._currentLevelRewards is None else int(self._currentLevelRewards.experienceReward)

    @property
    def itemsReward(self) -> list[list[int]]:
        self.initCurrentLevelRewards()
        return None if self._currentLevelRewards is None else self._currentLevelRewards.itemsReward

    @property
    def emotesReward(self) -> list[int]:
        self.initCurrentLevelRewards()
        return None if self._currentLevelRewards is None else self._currentLevelRewards.emotesReward

    @property
    def jobsReward(self) -> list[int]:
        self.initCurrentLevelRewards()
        return None if self._currentLevelRewards is None else self._currentLevelRewards.jobsReward

    @property
    def spellsReward(self) -> list[int]:
        self.initCurrentLevelRewards()
        return None if self._currentLevelRewards is None else self._currentLevelRewards.spellsReward

    @property
    def titlesReward(self) -> list[int]:
        self.initCurrentLevelRewards()
        return None if self._currentLevelRewards is None else self._currentLevelRewards.titlesReward

    @property
    def name(self) -> str:
        if not self._name:
            self._name = I18n.getText(self.nameId)
        return self._name

    @property
    def description(self) -> str:
        if not self._description:
            self._description = I18n.getText(self.descriptionId)
        return self._description

    @property
    def dialog(self) -> str:
        npcmsg: NpcMessage = None
        if self.dialogId < 1:
            return ""
        if not self._dialog:
            npcmsg = NpcMessage.getNpcMessageById(self.dialogId)
            self._dialog = DialogParamsDecoder.applyParams(npcmsg.message, npcmsg.messageParams) if npcmsg else ""
        return self._dialog

    @property
    def objectives(self) -> list["QuestObjective"]:
        from pydofus2.com.ankamagames.dofus.datacenter.quest.QuestObjective import QuestObjective

        i: int = 0
        if not self._objectives:
            self._objectives = list["QuestObjective"](len(self.objectiveIds), True)
            for i in range(len(self.objectiveIds)):
                self._objectives[i] = QuestObjective.getQuestObjectiveById(self.objectiveIds[i])
        return self._objectives

    def getKamasReward(self, pPlayerLevel: int) -> float:
        self.initCurrentLevelRewards()
        return (
            float(0)
            if self._currentLevelRewards is None
            else float(self._currentLevelRewards.getKamasReward(pPlayerLevel))
        )

    def getExperienceReward(self, pPlayerLevel: int, pXpBonus: int) -> float:
        self.initCurrentLevelRewards()
        return (
            float(0)
            if self._currentLevelRewards is None
            else float(self._currentLevelRewards.getExperienceReward(pPlayerLevel, pXpBonus))
        )

    def initCurrentLevelRewards(self) -> None:
        from pydofus2.com.ankamagames.dofus.datacenter.quest.QuestStepRewards import QuestStepRewards

        playerLvl: int = PlayedCharacterManager().limitedLevel
        if (
            self._currentLevelRewards == None
            or playerLvl < self._currentLevelRewards.levelMin
            and self._currentLevelRewards.levelMin != -1
            or playerLvl > self._currentLevelRewards.levelMax
            and self._currentLevelRewards.levelMax != -1
        ):
            self._currentLevelRewards = None
            for rewardsId in self.rewardsIds:
                rewards = QuestStepRewards.getQuestStepRewardsById(rewardsId)
                if (playerLvl >= rewards.levelMin or rewards.levelMin == -1) and (
                    playerLvl <= rewards.levelMax or rewards.levelMax == -1
                ):
                    self._currentLevelRewards = rewards

    idAccessors: IdAccessors = IdAccessors(getQuestStepById, getQuestSteps)
