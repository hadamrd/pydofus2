import math

import pydofus2.mapTools.MapTools as MapTools
from pydofus2.com.ankamagames.jerakine.map.IDataMapProvider import \
    IDataMapProvider
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint
from pydofus2.com.ankamagames.jerakine.types.zones.IZone import IZone


class ZRectangle(IZone):

    _radius: int = 0

    _radius2: int

    _minRadius: int = 2

    _dataMapProvider: IDataMapProvider

    _diagonalFree: bool = False

    def __init__(
        self,
        nMinRadius: int,
        nWidth: int,
        nHeight: int,
        dataMapProvider: IDataMapProvider,
    ):
        super().__init__()
        self.radius = nWidth
        self._radius2 = int(nHeight) if nHeight else int(nWidth)
        self.minRadius = nMinRadius
        self._dataMapProvider = dataMapProvider

    @property
    def radius(self) -> int:
        return self._radius

    @radius.setter
    def radius(self, n: int) -> None:
        self._radius = n

    @minRadius.setter
    def minRadius(self, r: int) -> None:
        self._minRadius = r

    @property
    def minRadius(self) -> int:
        return self._minRadius

    @property
    def direction(self) -> int:
        return None

    @direction.setter
    def direction(self, d: int) -> None:
        raise NotImplementedError()

    @property
    def diagonalFree(self) -> bool:
        return self._diagonalFree

    @diagonalFree.setter
    def diagonalFree(self, d: bool) -> None:
        self._diagonalFree = d

    @property
    def surface(self) -> int:
        return math.pow(self._radius + self._radius2 + 1, 2)

    def getCells(self, cellId: int = 0) -> list[int]:
        i: int = 0
        j: int = 0
        aCells: list[int] = list[int]()
        origin: MapPoint = MapPoint.fromCellId(cellId)
        x: int = origin.x
        y: int = origin.y
        if self._radius == 0 or self._radius2 == 0:
            if self._minRadius == 0 and not self._diagonalFree:
                aCells.append(cellId)
            return aCells
        for i in range(x - self._radius, x + self._radius + 1):
            for j in range(y - self._radius2, y + self._radius2 + 1):
                if not self._minRadius or abs(x - i) + abs(y - j) >= self._minRadius:
                    if not self._diagonalFree or abs(x - i) != abs(y - j):
                        if MapPoint.isInMap(i, j):
                            self.addCell(i, j, aCells)
        return aCells

    def addCell(self, x: int, y: int, cellMap: list[int]) -> None:
        if self._dataMapProvider == None or self._dataMapProvider.pointMov(x, y):
            cellMap.append(MapTools.getCellIdByCoord(x, y))
