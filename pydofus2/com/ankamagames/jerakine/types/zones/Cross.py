import pydofus2.mapTools.MapTools as MapTools
from pydofus2.com.ankamagames.jerakine.map.IDataMapProvider import \
    IDataMapProvider
from pydofus2.com.ankamagames.jerakine.types.enums.DirectionsEnum import \
    DirectionsEnum
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint
from pydofus2.com.ankamagames.jerakine.types.zones.IZone import IZone


class Cross(IZone):

    _radius: int = 0
    _minRadius: int = 0
    _dataMapProvider: IDataMapProvider
    _direction: int
    _diagonal: bool = False
    _allDirections: bool = False
    disabledDirection: list
    onlyPerpendicular: bool = False

    def __init__(self, nMinRadius: int, nMaxRadius: int, dataMapProvider: IDataMapProvider):
        self.disabledDirection = []
        super().__init__()
        self.minRadius = nMinRadius
        self.radius = nMaxRadius
        self._dataMapProvider = dataMapProvider

    @property
    def radius(self) -> int:
        return self._radius

    @radius.setter
    def radius(self, n: int) -> None:
        self._radius = n

    @property
    def surface(self) -> int:
        return self._radius * 4 + 1

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
    def diagonal(self) -> bool:
        return self._diagonal

    @diagonal.setter
    def diagonal(self, d: bool) -> None:
        self._diagonal = d

    @property
    def allDirections(self) -> bool:
        return self._allDirections

    @allDirections.setter
    def allDirections(self, d: bool) -> None:
        self._allDirections = d
        if self._allDirections:
            self.diagonal = False

    def getCells(self, cellId: int = 0) -> list[int]:
        aCells: list[int] = list[int]()
        if self._minRadius == 0:
            aCells.append(cellId)
        if self.onlyPerpendicular:
            if self._direction in [DirectionsEnum.DOWN_RIGHT, DirectionsEnum.UP_LEFT]:
                self.disabledDirection = [
                    DirectionsEnum.DOWN_RIGHT,
                    DirectionsEnum.UP_LEFT,
                ]
            elif self._direction in [DirectionsEnum.UP_RIGHT, DirectionsEnum.DOWN_LEFT]:
                self.disabledDirection = [
                    DirectionsEnum.UP_RIGHT,
                    DirectionsEnum.DOWN_LEFT,
                ]
            elif self._direction in [DirectionsEnum.DOWN, DirectionsEnum.UP]:
                self.disabledDirection = [DirectionsEnum.DOWN, DirectionsEnum.UP]
            elif self._direction in [DirectionsEnum.RIGHT, DirectionsEnum.LEFT]:
                self.disabledDirection = [DirectionsEnum.RIGHT, DirectionsEnum.LEFT]
        origin: MapPoint = MapPoint.fromCellId(cellId)
        x: int = origin.x
        y: int = origin.y
        for r in range(self._radius, self._minRadius, -1):
            if not self._diagonal:
                if MapPoint.isInMap(x + r, y) and DirectionsEnum.DOWN_RIGHT not in self.disabledDirection:
                    self.addCell(x + r, y, aCells)
                if MapPoint.isInMap(x - r, y) and DirectionsEnum.UP_LEFT not in self.disabledDirection:
                    self.addCell(x - r, y, aCells)
                if MapPoint.isInMap(x, y + r) and DirectionsEnum.UP_RIGHT not in self.disabledDirection:
                    self.addCell(x, y + r, aCells)
                if MapPoint.isInMap(x, y - r) and DirectionsEnum.DOWN_LEFT not in self.disabledDirection:
                    self.addCell(x, y - r, aCells)
            if self._diagonal or self._allDirections:
                if MapPoint.isInMap(x + r, y - r) and DirectionsEnum.DOWN not in self.disabledDirection:
                    self.addCell(x + r, y - r, aCells)
                if MapPoint.isInMap(x - r, y + r) and DirectionsEnum.UP not in self.disabledDirection:
                    self.addCell(x - r, y + r, aCells)
                if MapPoint.isInMap(x + r, y + r) and DirectionsEnum.RIGHT not in self.disabledDirection:
                    self.addCell(x + r, y + r, aCells)
                if MapPoint.isInMap(x - r, y - r) and DirectionsEnum.LEFT not in self.disabledDirection:
                    self.addCell(x - r, y - r, aCells)
        return aCells

    def addCell(self, x: int, y: int, cellMap: list[int]) -> None:
        if self._dataMapProvider is None or self._dataMapProvider.pointMov(x, y):
            cellMap.append(MapTools.getCellIdByCoord(x, y))
