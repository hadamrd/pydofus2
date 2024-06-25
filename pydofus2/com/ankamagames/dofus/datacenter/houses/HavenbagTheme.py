from pydofus2.com.ankamagames.dofus.misc.utils.GameDataQuery import GameDataQuery
from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class HavenbagTheme(IDataCenter):

    MODULE: str = "HavenbagThemes"

    _mapIds: list[int] = None

    id: int

    nameId: float

    mapId: float

    _name: str = None

    _furnitureIds: list[int]

    def __init__(self):
        super().__init__()

    @classmethod
    def getTheme(cls, id: int) -> "HavenbagTheme":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getAllThemes(cls) -> list["HavenbagTheme"]:
        return GameData().getObjects(cls.MODULE)

    @classmethod
    def isMapIdInHavenbag(cls, mapId: int) -> bool:
        if not cls._mapIds:
            cls._mapIds = [t.mapId for t in cls.getAllThemes()]
        return mapId in cls._mapIds

    @property
    def name(self) -> str:
        if not self._name:
            self._name = I18n.getText(self.nameId)
        return self._name

    @property
    def furnitureIds(self) -> list[int]:
        if not self._furnitureIds:
            self._furnitureIds = GameDataQuery.queryEquals(HavenbagFurniture, "themeId", self.id)
        return self._furnitureIds

    idAccessors: IdAccessors = IdAccessors(getTheme, None)
