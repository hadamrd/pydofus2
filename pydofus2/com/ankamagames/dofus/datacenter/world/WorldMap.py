from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter


class WorldMap(IDataCenter):

    MODULE: str = "WorldMaps"

    id: int

    nameId: int

    origineX: int

    origineY: int

    mapWidth: float

    mapHeight: float

    viewableEverywhere: bool

    minScale: float

    maxScale: float

    startScale: float

    totalWidth: int

    totalHeight: int

    zoom: list[str]

    visibleOnMap: bool

    _name: str = None

    def __init__(self):
        super().__init__()

    @staticmethod
    def getWorldMapById(id: int) -> "WorldMap":
        return GameData().getObject(WorldMap.MODULE, id)

    @staticmethod
    def getAllWorldMaps() -> list["WorldMap"]:
        return GameData().getObjects(WorldMap.MODULE)

    idAccessors: IdAccessors = IdAccessors(getWorldMapById, getAllWorldMaps)

    @property
    def name(self) -> str:
        if not self._name:
            self._name = I18n.getText(self.nameId)
        return self._name
