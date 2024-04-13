import math

import pydofus2.mapTools.MapTools as MapTools
from pydofus2.com.ankamagames.jerakine.map.IDataMapProvider import IDataMapProvider
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint
from pydofus2.com.ankamagames.jerakine.types.zones.DisplayZone import DisplayZone


class Lozenge(DisplayZone):

    _radius = 0
    _minRadius = 2

    def __init__(self, shape: int, alternativeSize: int, size: int, dataMapProvider: IDataMapProvider):
        super().__init__(shape, alternativeSize, size, dataMapProvider)
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
        return math.pow(self._radius + 1, 2) + math.pow(self._radius, 2)

    def getCells(self, cellId: int = 0) -> list[int]:
        cells = list[int]()
        origin = MapPoint.fromCellId(cellId)
        x = origin.x
        y = origin.y
        if self._radius == 0:
            if self._minRadius == 0:
                cells.append(cellId)
            return cells
        for radiusStep in range(int(self.radius), int(self._minRadius) - 1, -1):
            for i in range(-radiusStep, radiusStep + 1):
                for j in range(-radiusStep, radiusStep + 1):
                    if abs(i) + abs(j) == radiusStep:
                        xResult = x + i
                        yResult = y + j
                        if MapPoint.isInMap(xResult, yResult):
                            self.tryAddCell(xResult, yResult, cells)
        return cells
