from pydofus2.com.ankamagames.dofus.datacenter.quest.treasureHunt.PointOfInterestCategory import \
    PointOfInterestCategory
from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter


class PointOfInterest(IDataCenter):

    MODULE: str = "PointOfInterest"

    id: int
    nameId: int
    categoryId: int

    def __init__(self):
        self._name: str = None
        self._categoryActionLabel: str = None
        super().__init__()

    @classmethod
    def getPointOfInterestById(cls, id: int) -> "PointOfInterest":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getPointOfInterests(cls) -> list["PointOfInterest"]:
        return GameData().getObjects(cls.MODULE)

    @property
    def name(self) -> str:
        if not self._name:
            self._name = I18n.getUnDiacriticalText(self.nameId)
        return self._name

    @property
    def categoryActionLabel(self) -> str:
        if not self._categoryActionLabel:
            self._categoryActionLabel = PointOfInterestCategory.getPointOfInterestCategoryById(
                self.categoryId
            ).actionLabel
        return self._categoryActionLabel

    idAccessors: IdAccessors = IdAccessors(getPointOfInterestById, getPointOfInterests)
