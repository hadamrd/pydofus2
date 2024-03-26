import math

import pydofus2.mapTools.MapTools as MapTools
from pydofus2.com.ankamagames.jerakine.map.IDataMapProvider import \
    IDataMapProvider
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint
from pydofus2.com.ankamagames.jerakine.types.zones.IZone import IZone


class Lozenge(IZone):

    _radius = 0
    _minRadius = 2
    _dataMapProvider: IDataMapProvider

    def __init__(self, nMinRadius: int, nRadius: int, dataMapProvider: IDataMapProvider):
        super().__init__()
        self.radius = nRadius
        self.minRadius = nMinRadius
        self._dataMapProvider = dataMapProvider

    @property
    def radius(self) -> int:
        return self._radius

    @radius.setter
    def radius(self, n: int) -> None:
        self._radius = n

    @property
    def minRadius(self) -> int:
        return self._minRadius

    @minRadius.setter
    def minRadius(self, r: int) -> None:
        self._minRadius = r

    @property
    def direction(self) -> int:
        return None

    @direction.setter
    def direction(self, d: int) -> None:
        raise NotImplementedError()

    @property
    def surface(self) -> int:
        return math.pow(self._radius + 1, 2) + math.pow(self._radius, 2)

    def getCells(self, cellId: int = 0) -> list[int]:
        aCells: list[int] = list[int]()
        origin: MapPoint = MapPoint.fromCellId(cellId)
        x: int = origin.x
        y: int = origin.y
        if self._radius == 0:
            if self._minRadius == 0:
                aCells.append(cellId)
            return aCells
        for radiusStep in range(int(self.radius), int(self._minRadius) - 1, -1):
            for i in range(-radiusStep, radiusStep + 1):
                for j in range(-radiusStep, radiusStep + 1):
                    if abs(i) + abs(j) == radiusStep:
                        xResult = x + i
                        yResult = y + j
                        if MapPoint.isInMap(xResult, yResult):
                            self.addCell(xResult, yResult, aCells)
        return aCells

    def addCell(self, x: int, y: int, cellMap: list[int]) -> None:
        if self._dataMapProvider is None or self._dataMapProvider.pointMov(x, y):
            cellMap.append(MapTools.getCellIdByCoord(x, y))
