import math

import pydofus2.mapTools.MapTools as MapTools
from pydofus2.com.ankamagames.jerakine.map.IDataMapProvider import \
    IDataMapProvider
from pydofus2.com.ankamagames.jerakine.types.enums.DirectionsEnum import \
    DirectionsEnum
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint
from pydofus2.com.ankamagames.jerakine.types.zones.IZone import IZone


class Cone(IZone):

    _radius: int = 0

    _minRadius: int = 0

    _nDirection: int = 1

    _dataMapProvider: IDataMapProvider

    def __init__(self, nMinRadius: int, nRadius: int, dataMapProvider: IDataMapProvider):
        super().__init__()
        self.radius = nRadius
        self.minRadius = nMinRadius
        self._dataMapProvider = dataMapProvider

    @radius.setter
    def radius(self, n: int) -> None:
        self._radius = n

    @property
    def radius(self) -> int:
        return self._radius

    @property
    def minRadius(self) -> int:
        return self._minRadius

    @minRadius.setter
    def minRadius(self, r: int) -> None:
        self._minRadius = r

    @property
    def direction(self) -> int:
        return self._nDirection

    @direction.setter
    def direction(self, d: int) -> None:
        self._nDirection = d

    @property
    def surface(self) -> int:
        return math.pow(self._radius + 1, 2)

    def getCells(self, cellId: int = 0) -> list[int]:
        i: int = 0
        j: int = 0
        aCells: list[int] = list[int]()
        origin: MapPoint = MapPoint.fromCellId(cellId)
        x: int = origin.x
        y: int = origin.y
        if self._radius == 0:
            if self._minRadius == 0:
                aCells.append(cellId)
            return aCells
        step: int = 0
        if self._nDirection is DirectionsEnum.UP_LEFT:
            for i in range(x, x - self._radius - 1, -1):
                for j in range(-step, step + 1):
                    if not self._minRadius or abs(x - i) + abs(j) >= self._minRadius:
                        if MapPoint.isInMap(i, j + y):
                            self.addCell(i, j + y, aCells)
                step += 1
        if self._nDirection == DirectionsEnum.DOWN_LEFT:
            for j in range(y, y - self._radius - 1):
                for i in range(-step, step + 1):
                    if not self._minRadius or abs(i) + abs(y - j) >= self._minRadius:
                        if MapPoint.isInMap(i + x, j):
                            self.addCell(i + x, j, aCells)
                step += 1
        if self._nDirection == DirectionsEnum.DOWN_RIGHT:
            for i in range(x, x + self._radius + 1):
                for j in range(-step, step + 1):
                    if not self._minRadius or abs(x - i) + abs(j) >= self._minRadius:
                        if MapPoint.isInMap(i, j + y):
                            self.addCell(i, j + y, aCells)
                step += 1
        if self._nDirection == DirectionsEnum.UP_RIGHT:
            for j in range(y, y + self._radius + 1):
                for i in range(-step, step + 1):
                    if not self._minRadius or abs(i) + abs(y - j) >= self._minRadius:
                        if MapPoint.isInMap(i + x, j):
                            self.addCell(i + x, j, aCells)
                step += 1
        return aCells

    def addCell(self, x: int, y: int, cellMap: list[int]) -> None:
        if self._dataMapProvider == None or self._dataMapProvider.pointMov(x, y):
            cellMap.append(MapTools.getCellIdByCoord(x, y))
