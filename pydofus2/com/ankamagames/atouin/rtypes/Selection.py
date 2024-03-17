from pydofus2.com.ankamagames.atouin.managers.MapDisplayManager import \
    MapDisplayManager
from pydofus2.com.ankamagames.jerakine.types.zones.IZone import IZone


class Selection:
    _mapId: float = None

    cells: list[int]

    cellId: int

    visible: bool

    zone: IZone = None

    def __init__(self):
        super().__init__()

    @property
    def mapId(self) -> float:
        if self._mapId is None:
            return MapDisplayManager().currentMapPoint.mapId
        return self._mapId

    @mapId.setter
    def mapId(self, id: float) -> None:
        self._mapId = id

    def update(self, pUpdateStrata: bool = False) -> None:
        self.visible = True

    def remove(self, aCells: list[int] = None) -> None:
        pass

    def isInside(self, cellId: int) -> bool:
        return cellId in self.cells
