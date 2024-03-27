import math

from pydofus2.com.ankamagames.jerakine.types.zones.DisplayZone import DisplayZone
from pydofus2.com.ankamagames.jerakine.utils.display.spellZone.SpellShapeEnum import SpellShapeEnum
import pydofus2.mapTools.MapTools as MapTools
from pydofus2.com.ankamagames.jerakine.map.IDataMapProvider import \
    IDataMapProvider
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint


class ZRectangle(DisplayZone):

    _radius: int = 0
    _radius2: int
    _minRadius: int = 2
    _diagonalFree: bool = False

    def __init__(
        self,
        minRadius:int, alternativeSize:int, size:int, isDiagonalFree:bool, dataMapProvider:IDataMapProvider
    ):
        super().__init__(SpellShapeEnum.UNKNOWN, alternativeSize, size, dataMapProvider)
        self._diagonalFree = isDiagonalFree
        self._width = alternativeSize
        self._height = size if size else alternativeSize
        self._minRadius = minRadius

    @property
    def radius(self) -> int:
        return self._radius

    @property
    def minRadius(self) -> int:
        return self._minRadius

    @property
    def diagonalFree(self) -> bool:
        return self._diagonalFree

    @property
    def surface(self) -> int:
        return math.pow(self._width + self._height + 1, 2)

    def getCells(self, cellId: int = 0) -> list[int]:
        i: int = 0
        j: int = 0
        cells: list[int] = list[int]()
        origin: MapPoint = MapPoint.fromCellId(cellId)
        x: int = origin.x
        y: int = origin.y
        if self._width == 0 or self._height == 0:
            if self._minRadius == 0 and not self._diagonalFree:
                cells.append(cellId)
            return cells
        for i in range(x - self._width, x + self._width + 1):
            for j in range(y - self._height, y + self._height + 1):
                if not self._minRadius or abs(x - i) + abs(y - j) >= self._minRadius:
                    if not self._diagonalFree or abs(x - i) != abs(y - j):
                        if MapPoint.isInMap(i, j):
                            self.tryAddCell(i, j, cells)
        return cells
