from pydofus2.com.ankamagames.jerakine.types.zones.DisplayZone import DisplayZone
from pydofus2.com.ankamagames.jerakine.utils.display.spellZone.SpellShapeEnum import SpellShapeEnum
from pydofus2.com.ankamagames.jerakine.map.IDataMapProvider import \
    IDataMapProvider
from pydofus2.com.ankamagames.jerakine.types.enums.DirectionsEnum import \
    DirectionsEnum
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint


class Cross(DisplayZone):

    _radius: int = 0
    _minRadius: int = 0
    _diagonal: bool = False
    _allDirections: bool = False
    _disabledDirection = list[int]()
    _onlyPerpendicular: bool = False

    def __init__(self, shape:int, alternativeSize:int, size:int, dataMapProvider:IDataMapProvider, diagonal:bool = False, allDirections:bool = False):
        self._disabledDirection = []
        super().__init__(shape, size, dataMapProvider)
        self._minRadius = alternativeSize
        self._radius = size
        self._onlyPerpendicular = (shape == SpellShapeEnum.T or shape == SpellShapeEnum.minus)
        self._diagonal = not allDirections and diagonal
        self._allDirections = allDirections

    @property
    def radius(self) -> int:
        return self._radius

    @property
    def surface(self) -> int:
        return self._radius * 4 + 1

    @property
    def minRadius(self) -> int:
        return self._minRadius

    @property
    def diagonal(self) -> bool:
        return self._diagonal

    @property
    def allDirections(self) -> bool:
        return self._allDirections

    def getCells(self, cellId: int = 0) -> list[int]:
        cells = list[int]()
        if self._minRadius == 0:
            cells.append(cellId)
        if self._onlyPerpendicular:
            if self._direction in [DirectionsEnum.DOWN_RIGHT, DirectionsEnum.UP_LEFT]:
                self._disabledDirection = [
                    DirectionsEnum.DOWN_RIGHT,
                    DirectionsEnum.UP_LEFT,
                ]
            elif self._direction in [DirectionsEnum.UP_RIGHT, DirectionsEnum.DOWN_LEFT]:
                self._disabledDirection = [
                    DirectionsEnum.UP_RIGHT,
                    DirectionsEnum.DOWN_LEFT,
                ]
            elif self._direction in [DirectionsEnum.DOWN, DirectionsEnum.UP]:
                self._disabledDirection = [DirectionsEnum.DOWN, DirectionsEnum.UP]
            elif self._direction in [DirectionsEnum.RIGHT, DirectionsEnum.LEFT]:
                self._disabledDirection = [DirectionsEnum.RIGHT, DirectionsEnum.LEFT]
        origin: MapPoint = MapPoint.fromCellId(cellId)
        x: int = origin.x
        y: int = origin.y
        for r in range(self._radius, self._minRadius, -1):
            if not self._diagonal:
                if MapPoint.isInMap(x + r, y) and DirectionsEnum.DOWN_RIGHT not in self._disabledDirection:
                    self.tryAddCell(x + r, y, cells)
                if MapPoint.isInMap(x - r, y) and DirectionsEnum.UP_LEFT not in self._disabledDirection:
                    self.tryAddCell(x - r, y, cells)
                if MapPoint.isInMap(x, y + r) and DirectionsEnum.UP_RIGHT not in self._disabledDirection:
                    self.tryAddCell(x, y + r, cells)
                if MapPoint.isInMap(x, y - r) and DirectionsEnum.DOWN_LEFT not in self._disabledDirection:
                    self.tryAddCell(x, y - r, cells)
            if self._diagonal or self._allDirections:
                if MapPoint.isInMap(x + r, y - r) and DirectionsEnum.DOWN not in self._disabledDirection:
                    self.tryAddCell(x + r, y - r, cells)
                if MapPoint.isInMap(x - r, y + r) and DirectionsEnum.UP not in self._disabledDirection:
                    self.tryAddCell(x - r, y + r, cells)
                if MapPoint.isInMap(x + r, y + r) and DirectionsEnum.RIGHT not in self._disabledDirection:
                    self.tryAddCell(x + r, y + r, cells)
                if MapPoint.isInMap(x - r, y - r) and DirectionsEnum.LEFT not in self._disabledDirection:
                    self.tryAddCell(x - r, y - r, cells)
        return cells
