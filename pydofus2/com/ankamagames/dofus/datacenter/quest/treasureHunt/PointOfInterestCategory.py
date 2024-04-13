from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class PointOfInterestCategory(IDataCenter):

    MODULE: str = "PointOfInterestCategory"

    id: int
    actionLabelId: int

    _actionLabel: str = None

    def __init__(self):
        super().__init__()

    @classmethod
    def getPointOfInterestCategoryById(cls, id: int) -> "PointOfInterestCategory":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getPointOfInterestCategories(cls) -> list["PointOfInterestCategory"]:
        return GameData().getObjects(cls.MODULE)

    @property
    def actionLabel(self) -> str:
        if not self._actionLabel:
            self._actionLabel = I18n.getText(self.actionLabelId)
        return self._actionLabel

    idAccessors: IdAccessors = IdAccessors(getPointOfInterestCategoryById, getPointOfInterestCategories)
