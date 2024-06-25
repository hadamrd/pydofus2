from pydofus2.com.ankamagames.dofus.datacenter.quest.QuestStep import QuestStep
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class QuestStepRewards(IDataCenter):

    MODULE: str = "QuestStepRewards"

    id: int

    stepId: int

    levelMin: int

    levelMax: int

    kamasRatio: float

    experienceRatio: float

    kamasScaleWithPlayerLevel: bool

    itemsReward: list[list[int]]

    emotesReward: list[int]

    jobsReward: list[int]

    spellsReward: list[int]

    titlesReward: list[int]

    _questStep: QuestStep = None

    def __init__(self):
        super().__init__()

    @classmethod
    def getQuestStepRewardsById(cls, id: int) -> "QuestStepRewards":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getQuestStepRewards(cls) -> list["QuestStepRewards"]:
        return GameData().getObjects(cls.MODULE)

    @property
    def questStep(self) -> QuestStep:
        if not self._questStep:
            self._questStep = QuestStep.getQuestStepById(self.stepId)
        return self._questStep

    @property
    def kamasReward(self) -> float:
        return RoleplayManager().getKamasReward(
            self.kamasScaleWithPlayerLevel, self.questStep.optimalLevel, self.kamasRatio, self.questStep.duration
        )

    @property
    def experienceReward(self) -> int:
        return RoleplayManager().getExperienceReward(
            PlayedCharacterManager().limitedLevel,
            PlayedCharacterManager().experiencePercent,
            self.questStep.optimalLevel,
            self.experienceRatio,
            self.questStep.duration,
        )

    def getKamasReward(self, pPlayerLevel: int) -> float:
        return RoleplayManager().getKamasReward(
            self.kamasScaleWithPlayerLevel,
            self.questStep.optimalLevel,
            self.kamasRatio,
            self.questStep.duration,
            pPlayerLevel,
        )

    def getExperienceReward(self, pPlayerLevel: int, pXpBonus: int) -> float:
        return RoleplayManager().getExperienceReward(
            pPlayerLevel, pXpBonus, self.questStep.optimalLevel, self.experienceRatio, self.questStep.duration
        )

    idAccessors: IdAccessors = IdAccessors(getQuestStepRewardsById, getQuestStepRewards)
