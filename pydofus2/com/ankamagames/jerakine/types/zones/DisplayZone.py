from pydofus2.com.ankamagames.jerakine.map.IDataMapProvider import IDataMapProvider
from pydofus2.mapTools import MapTools


class DisplayZone:
    def __init__(self, shape: int, other_size: int, size: int, dataMapProvider:IDataMapProvider=None):
        self._shape = shape
        self._otherSize = other_size
        self._size = size
        self._dataMapProvider:IDataMapProvider = dataMapProvider

    @property
    def otherSize(self) -> int:
        return self._otherSize

    @property
    def size(self) -> int:
        return self._size

    @property
    def shape(self) -> int:
        return self._shape

    @property
    def surface(self) -> int:
        return 0

    @property
    def isInfinite(self) -> bool:
        return self._size == 63

    @property
    def direction(self) -> int:
        return self._direction

    @direction.setter
    def direction(self, direction: int) -> None:
        self._direction = direction

    def getCells(self, cellId: int = 0) -> list:
        return []

    def tryAddCell(self, x: int, y: int, cell_map: list) -> None:
        if self._dataMapProvider is None or self._dataMapProvider.pointMov(x, y):
            cell_map.append(MapTools.getCellIdByCoord(x,y))