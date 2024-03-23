from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.GroupItemCriterion import GroupItemCriterion
from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger


class AchievementCategory:
    MODULE = "AchievementCategories"

    def __init__(self):
        self.id = 0
        self.nameId = 0
        self.parentId = 0
        self.icon = ""
        self.order = 0
        self.color = ""
        self.achievementIds = []
        self.visibilityCriterion = ""
        self._name = ""
        self._achievements = None

    @staticmethod
    def getAchievementCategoryById(id) -> "AchievementCategory":
        return GameData().getObject(AchievementCategory.MODULE, id)

    @staticmethod
    def getAchievementCategories() -> list["AchievementCategory"]:
        return GameData().getObjects(AchievementCategory.MODULE)

    @property
    def name(self):
        if not self._name:
            self._name = I18n.getText(self.nameId)
        return self._name

    @property
    def achievements(self):
        from pydofus2.com.ankamagames.dofus.datacenter.quest.Achievement import Achievement

        if not self._achievements:
            self._achievements = [
                Achievement.getAchievementById(achievementId) for achievementId in self.achievementIds
            ]
        return self._achievements

    @property
    def visible(self):
        if self.visibilityCriterion is None:
            Logger().warning("Visibility criterion is null for category " + str(self.id))
            self.visibilityCriterion = ""
        gic = GroupItemCriterion(self.visibilityCriterion)
        return gic.isRespected

    idAccessors = IdAccessors(getAchievementCategoryById, getAchievementCategories)
