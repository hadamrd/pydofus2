import pydofus2.mapTools.MapTools as MapTools
from pydofus2.com.ankamagames.jerakine.map.IDataMapProvider import \
    IDataMapProvider
from pydofus2.com.ankamagames.jerakine.types.enums.DirectionsEnum import \
    DirectionsEnum
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint
from pydofus2.com.ankamagames.jerakine.types.zones.IZone import IZone


class Line(IZone):

    _radius: int = 0

    _minRadius: int = 0

    _nDirection: int = 1

    _dataMapProvider: IDataMapProvider

    _fromCaster: bool

    _stopAtTarget: bool

    _casterCellId: int

    def __init__(self, nRadius: int, dataMapProvider: IDataMapProvider):
        super().__init__()
        self.radius = nRadius
        self._dataMapProvider = dataMapProvider

    @property
    def radius(self) -> int:
        return self._radius

    @radius.setter
    def radius(self, n: int) -> None:
        self._radius = n

    @property
    def surface(self) -> int:
        return self._radius + 1

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
    def fromCaster(self) -> bool:
        return self._fromCaster

    @fromCaster.setter
    def fromCaster(self, b: bool) -> None:
        self._fromCaster = b

    @property
    def stopAtTarget(self) -> bool:
        return self._stopAtTarget

    @stopAtTarget.setter
    def stopAtTarget(self, b: bool) -> None:
        self._stopAtTarget = b

    @property
    def casterCellId(self) -> int:
        return self._casterCellId

    @casterCellId.setter
    def casterCellId(self, c: int) -> None:
        self._casterCellId = c

    def getCells(self, cellId: int = 0) -> list[int]:
        added: bool = False
        distance: int = 0
        aCells: list[int] = list[int]()
        origin: MapPoint = (
            MapPoint.fromCellId(cellId) if not self._fromCaster else MapPoint.fromCellId(self.casterCellId)
        )
        x: int = origin.x
        y: int = origin.y
        length: int = int(self._radius) if not self.fromCaster else int(self._radius + self._minRadius - 1)
        if self.fromCaster and self.stopAtTarget:
            distance = origin.distanceToCell(MapPoint.fromCellId(cellId))
            length = int(distance) if distance < length else int(length)
        for r in range(self._minRadius, length + 1):
            if self._nDirection == DirectionsEnum.LEFT:
                if MapPoint.isInMap(x - r, y - r):
                    self.addCell(x - r, y - r, aCells)
            elif self._nDirection == DirectionsEnum.UP:
                if MapPoint.isInMap(x - r, y + r):
                    self.addCell(x - r, y + r, aCells)
            elif self._nDirection == DirectionsEnum.RIGHT:
                if MapPoint.isInMap(x + r, y + r):
                    self.addCell(x + r, y + r, aCells)
            elif self._nDirection == DirectionsEnum.DOWN:
                if MapPoint.isInMap(x + r, y - r):
                    self.addCell(x + r, y - r, aCells)
            elif self._nDirection == DirectionsEnum.UP_LEFT:
                if MapPoint.isInMap(x - r, y):
                    self.addCell(x - r, y, aCells)
            elif self._nDirection == DirectionsEnum.DOWN_LEFT:
                if MapPoint.isInMap(x, y - r):
                    self.addCell(x, y - r, aCells)
            elif self._nDirection == DirectionsEnum.DOWN_RIGHT:
                if MapPoint.isInMap(x + r, y):
                    self.addCell(x + r, y, aCells)
            elif self._nDirection == DirectionsEnum.UP_RIGHT:
                if MapPoint.isInMap(x, y + r):
                    self.addCell(x, y + r, aCells)
        return aCells

    def addCell(self, x: int, y: int, cellMap: list[int]) -> bool:
        if self._dataMapProvider is None or self._dataMapProvider.pointMov(x, y):
            cellMap.append(MapTools.getCellIdByCoord(x, y))
            return True
        return False
