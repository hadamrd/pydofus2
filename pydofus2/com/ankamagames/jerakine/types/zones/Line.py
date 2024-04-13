import pydofus2.mapTools.MapTools as MapTools
from pydofus2.com.ankamagames.jerakine.map.IDataMapProvider import IDataMapProvider
from pydofus2.com.ankamagames.jerakine.types.enums.DirectionsEnum import DirectionsEnum
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint
from pydofus2.com.ankamagames.jerakine.types.zones.DisplayZone import DisplayZone


class Line(DisplayZone):

    _radius: int = 0
    _minRadius: int = 0
    _fromCaster: bool
    _stopAtTarget: bool
    _casterCellId: int

    def __init__(
        self,
        shape: int,
        alternativeSize: int,
        size: int,
        dataMapProvider: IDataMapProvider,
        fromCaster: bool = False,
        stopAtTarget: bool = False,
        casterCellId: int = 0,
    ):
        super().__init__(shape, alternativeSize, size, dataMapProvider)
        self._radius = size
        self._minRadius = alternativeSize
        self._fromCaster = fromCaster
        self._stopAtTarget = stopAtTarget
        self._casterCellId = casterCellId

    @property
    def radius(self) -> int:
        return self._radius

    @property
    def surface(self) -> int:
        return self._radius + 1

    @property
    def isFromCaster(self) -> bool:
        return self._fromCaster

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
        if self._fromCaster and self._stopAtTarget:
            distance = origin.distanceToCell(MapPoint.fromCellId(cellId))
            length = int(distance) if distance < length else int(length)
        for r in range(self._minRadius, length + 1):
            if self._direction == DirectionsEnum.LEFT:
                if MapPoint.isInMap(x - r, y - r):
                    self.tryAddCell(x - r, y - r, aCells)
            elif self._direction == DirectionsEnum.UP:
                if MapPoint.isInMap(x - r, y + r):
                    self.tryAddCell(x - r, y + r, aCells)
            elif self._direction == DirectionsEnum.RIGHT:
                if MapPoint.isInMap(x + r, y + r):
                    self.tryAddCell(x + r, y + r, aCells)
            elif self._direction == DirectionsEnum.DOWN:
                if MapPoint.isInMap(x + r, y - r):
                    self.tryAddCell(x + r, y - r, aCells)
            elif self._direction == DirectionsEnum.UP_LEFT:
                if MapPoint.isInMap(x - r, y):
                    self.tryAddCell(x - r, y, aCells)
            elif self._direction == DirectionsEnum.DOWN_LEFT:
                if MapPoint.isInMap(x, y - r):
                    self.tryAddCell(x, y - r, aCells)
            elif self._direction == DirectionsEnum.DOWN_RIGHT:
                if MapPoint.isInMap(x + r, y):
                    self.tryAddCell(x + r, y, aCells)
            elif self._direction == DirectionsEnum.UP_RIGHT:
                if MapPoint.isInMap(x, y + r):
                    self.tryAddCell(x, y + r, aCells)
        return aCells
