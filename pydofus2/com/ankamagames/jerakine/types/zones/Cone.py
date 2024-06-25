import math

from pydofus2.com.ankamagames.jerakine.map.IDataMapProvider import IDataMapProvider
from pydofus2.com.ankamagames.jerakine.types.enums.DirectionsEnum import DirectionsEnum
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint
from pydofus2.com.ankamagames.jerakine.types.zones.DisplayZone import DisplayZone
from pydofus2.com.ankamagames.jerakine.utils.display.spellZone.SpellShapeEnum import SpellShapeEnum


class Cone(DisplayZone):
    _radius: int = 0
    _minRadius: int = 0

    def __init__(self, alternativeSize: int, size: int, dataMapProvider: IDataMapProvider):
        super().__init__(SpellShapeEnum.V, alternativeSize, size, dataMapProvider)
        self._minRadius = alternativeSize
        self._radius = size

    @property
    def radius(self) -> int:
        return self._radius

    @property
    def minRadius(self) -> int:
        return self._minRadius

    @property
    def surface(self) -> int:
        return math.pow(self._radius + 1, 2)

    def getCells(self, cellId: int = 0) -> list[int]:
        i: int = 0
        j: int = 0
        cells: list[int] = list[int]()
        origin: MapPoint = MapPoint.fromCellId(cellId)
        x: int = origin.x
        y: int = origin.y
        if self._radius == 0:
            if self._minRadius == 0:
                cells.append(cellId)
            return cells
        step: int = 0
        if self._direction == DirectionsEnum.UP_LEFT:
            for i in range(x, x - self._radius - 1, -1):
                for j in range(-step, step + 1):
                    if not self._minRadius or abs(x - i) + abs(j) >= self._minRadius:
                        if MapPoint.isInMap(i, j + y):
                            self.tryAddCell(i, j + y, cells)
                step += 1
        if self._direction == DirectionsEnum.DOWN_LEFT:
            for j in range(y, y - self._radius - 1):
                for i in range(-step, step + 1):
                    if not self._minRadius or abs(i) + abs(y - j) >= self._minRadius:
                        if MapPoint.isInMap(i + x, j):
                            self.tryAddCell(i + x, j, cells)
                step += 1
        if self._direction == DirectionsEnum.DOWN_RIGHT:
            for i in range(x, x + self._radius + 1):
                for j in range(-step, step + 1):
                    if not self._minRadius or abs(x - i) + abs(j) >= self._minRadius:
                        if MapPoint.isInMap(i, j + y):
                            self.tryAddCell(i, j + y, cells)
                step += 1
        if self._direction == DirectionsEnum.UP_RIGHT:
            for j in range(y, y + self._radius + 1):
                for i in range(-step, step + 1):
                    if not self._minRadius or abs(i) + abs(y - j) >= self._minRadius:
                        if MapPoint.isInMap(i + x, j):
                            self.tryAddCell(i + x, j, cells)
                step += 1
        return cells
