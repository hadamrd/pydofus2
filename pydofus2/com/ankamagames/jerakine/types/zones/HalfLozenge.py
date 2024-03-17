import pydofus2.mapTools.MapTools as MapTools
from pydofus2.com.ankamagames.jerakine.map.IDataMapProvider import \
    IDataMapProvider
from pydofus2.com.ankamagames.jerakine.types.enums.DirectionsEnum import \
    DirectionsEnum
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint
from pydofus2.com.ankamagames.jerakine.types.zones.IZone import IZone


class HalfLozenge(IZone):

    _radius: int = 0

    _minRadius: int = 2

    _direction: int = 6

    _dataMapProvider: IDataMapProvider

    def __init__(self, minRadius: int, nRadius: int, dataMapProvider: IDataMapProvider):
        super().__init__()
        self.radius = nRadius
        self._minRadius = minRadius
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
        return self._direction

    @direction.setter
    def direction(self, d: int) -> None:
        self._direction = d

    @property
    def direction(self) -> int:
        return self._direction

    @property
    def surface(self) -> int:
        return self._radius * 2 + 1

    def getCells(self, cellId: int = 0) -> list[int]:
        i: int = 0
        aCells: list[int] = list[int]()
        origin: MapPoint = MapPoint.fromCellId(cellId)
        x: int = origin.x
        y: int = origin.y
        if self._minRadius == 0:
            aCells.append(cellId)
        for i in range(1, self._radius + 1):
            if self._direction == DirectionsEnum.UP_LEFT:
                self.addCell(x + i, y + i, aCells)
                self.addCell(x + i, y - i, aCells)
            elif self._direction == DirectionsEnum.UP_RIGHT:
                self.addCell(x - i, y - i, aCells)
                self.addCell(x + i, y - i, aCells)
            elif self._direction == DirectionsEnum.DOWN_RIGHT:
                self.addCell(x - i, y + i, aCells)
                self.addCell(x - i, y - i, aCells)
            elif self._direction == DirectionsEnum.DOWN_LEFT:
                self.addCell(x - i, y + i, aCells)
                self.addCell(x + i, y + i, aCells)
        return aCells

    def addCell(self, x: int, y: int, cellMap: list[int]) -> None:
        if self._dataMapProvider == None or self._dataMapProvider.pointMov(x, y):
            cellMap.append(MapTools.getCellIdByCoord(x, y))
