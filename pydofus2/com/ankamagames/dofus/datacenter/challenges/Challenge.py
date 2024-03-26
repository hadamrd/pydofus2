from pydofus2.com.ankamagames.dofus.datacenter.quest.AchievementObjective import \
    AchievementObjective
from pydofus2.com.ankamagames.dofus.misc.utils.GameDataQuery import \
    GameDataQuery
from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.data.XmlConfig import XmlConfig
from pydofus2.com.ankamagames.jerakine.types.Uri import Uri


class Challenge:
    MODULE = "Challenges"

    def __init__(self):
        self.id = 0
        self.nameId = 0
        self.descriptionId = 0
        self.incompatibleChallenges = []  # Vector in AS3 is equivalent to a list in Python
        self.categoryId = 0
        self.iconId = 0
        self.activationCriterion = ""
        self.completionCriterion = ""
        self.targetMonsterId = 0
        self._name = ""
        self._description = ""
        self._boundAchievements = None
        self._uri = None

    @staticmethod
    def getChallengeById(challenge_id) -> "Challenge":
        return GameData().getObject(Challenge.MODULE, challenge_id)

    @staticmethod
    def getChallenges() -> list["Challenge"]:
        return GameData().getObjects(Challenge.MODULE)

    @property
    def name(self):
        if not self._name:
            self._name = I18n.getText(self.nameId)
        return self._name

    @property
    def description(self):
        if not self._description:
            self._description = I18n.getText(self.descriptionId)
        return self._description

    @property
    def boundAchievements(self):
        if self._boundAchievements is not None:
            return self._boundAchievements

        achievementObjectiveIds = GameDataQuery().queryString(AchievementObjective, "criterion", "EH>" + str(self.id))
        achievements = []

        for objective_id in achievementObjectiveIds:
            achievementObjective = AchievementObjective.getAchievementObjectiveById(objective_id)
            criterionId = int(achievementObjective.criterion.split("EH>")[1].split(",")[0])
            if achievementObjective and criterionId == self.id:
                from pydofus2.com.ankamagames.dofus.datacenter.quest.Achievement import \
                    Achievement

                achievement = Achievement.getAchievementById(achievementObjective.achievementId)
                if achievement:
                    achievements.append(achievement)

        self._boundAchievements = achievements
        return self._boundAchievements

    @property
    def iconUri(self):
        if not self._uri:
            basePath = XmlConfig().getEntry("config.gfx.path.challenges")
            if basePath is None:
                return None
            self._uri = Uri(basePath + str(self.iconId) + ".png")
        return self._uri

    def getTurnsNumberForCompletion(self):
        if not self.completionCriterion:
            return float("nan")
        for criteria in self.completionCriterion.split("&"):
            if "ST<" in criteria:
                criteriaData = criteria.split("ST<")
                if len(criteriaData) < 2:
                    return float("nan")
                return float(criteriaData[1])
        return float("nan")

    def getBoundBossId(self):
        if not self.activationCriterion:
            return float("nan")
        for criteria in self.activationCriterion.split("&"):
            if "GM>" in criteria:
                criteriaData = criteria.split(",")
                if len(criteriaData) < 2:
                    return float("nan")
                return float(criteriaData[1])
        return float("nan")

    def getTargetMonsterId(self):
        return self.targetMonsterId

    def getPlayersNumberType(self):
        if not self.activationCriterion:
            return float("nan")
        for criteria in self.activationCriterion.split("&"):
            if "GN<" in criteria:
                criteriaData = criteria.split("<")
                if len(criteriaData) < 2:
                    return float("nan")
                criteriaParams = criteriaData[1]
                if criteriaParams:
                    return float(criteriaParams.split(",")[0])
                return float("nan")
        return float("nan")

    idAccessors = IdAccessors(getChallengeById, getChallenges)
