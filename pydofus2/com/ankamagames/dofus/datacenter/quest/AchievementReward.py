from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.GroupItemCriterion import GroupItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.LevelItemCriterion import LevelItemCriterion
from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData


class AchievementReward:
    MODULE = "AchievementRewards"

    def __init__(self):
        self.id = 0
        self.achievementId = 0
        self.criteria = ""
        self.kamasRatio = 0.0
        self.experienceRatio = 0.0
        self.kamasScaleWithPlayerLevel = False
        self.itemsReward = []
        self.itemsQuantityReward = []
        self.emotesReward = []
        self.spellsReward = []
        self.titlesReward = []
        self.ornamentsReward = []
        self.guildPoints = 0
        self._achievement = None
        self._conditions = None

    @staticmethod
    def getAchievementRewardById(id) -> "AchievementReward":
        return GameData.getObject(AchievementReward.MODULE, id)

    @staticmethod
    def getAchievementRewards() -> list["AchievementReward"]:
        return GameData().getObjects(AchievementReward.MODULE)

    @property
    def achievement(self):
        if not self._achievement:
            from pydofus2.com.ankamagames.dofus.datacenter.quest.Achievement import Achievement

            self._achievement = Achievement.getAchievementById(self.achievementId)
        return self._achievement

    @property
    def conditions(self):
        if not self.criteria:
            return None
        if not self._conditions:
            self._conditions = GroupItemCriterion(self.criteria)
        return self._conditions

    def getGuildPointsReward(self):
        return self.guildPoints

    def getKamasReward(self, pPlayerLevel):
        return RoleplayManager().getKamasReward(
            self.kamasScaleWithPlayerLevel, self.achievement.level, self.kamasRatio, 1, pPlayerLevel
        )

    def getExperienceReward(self, pPlayerLevel, pXpBonus):
        return RoleplayManager().getExperienceReward(
            pPlayerLevel, pXpBonus, self.achievement.level, self.experienceRatio
        )

    def isConditionRespectedForSpecificLevel(self, level):
        if self.conditions is None:
            return True
        if len(self.conditions.criteria) == 1 and isinstance(self.conditions.criteria[0], ItemCriterion):
            if isinstance(self.conditions.criteria[0], LevelItemCriterion):
                levelCriterion = self.conditions.criteria[0]
                return levelCriterion.operator.compare(level, levelCriterion.criterionValue)
            return self.conditions.criteria[0].isRespected

        if self.conditions.operators and self.conditions.operators[0] == "|":
            for criterion in self.conditions.criteria:
                if isinstance(criterion, LevelItemCriterion):
                    levelCriterionResult = criterion.operator.compare(level, criterion.criterionValue)
                    if levelCriterionResult:
                        return True
                elif criterion.isRespected:
                    return True
            return False

        for criterion in self.conditions.criteria:
            if isinstance(criterion, LevelItemCriterion):
                levelCriterionResult = criterion.operator.compare(level, criterion.criterionValue)
                if not levelCriterionResult:
                    return False
            elif not criterion.isRespected:
                return False

        return True

    def __str__(self):
        text = f"Reward {self.id} ({self.criteria}) : "
        if self.kamasRatio > 0:
            text += f"     kamasRatio {self.kamasRatio}   (scale with player ? {self.kamasScaleWithPlayerLevel})"
        # Similar formatting for other attributes
        return text

    idAccessors = IdAccessors(getAchievementRewardById, getAchievementRewards)
