from pydofus2.com.ankamagames.jerakine.types.zones.DisplayZone import DisplayZone
from pydofus2.com.ankamagames.jerakine.utils.display.spellZone.SpellShapeEnum import SpellShapeEnum
from pydofus2.com.ankamagames.jerakine.map.IDataMapProvider import IDataMapProvider
from pydofus2.com.ankamagames.jerakine.types.enums.DirectionsEnum import DirectionsEnum
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint

class HalfLozenge(DisplayZone):

    _radius: int = 0

    _minRadius: int = 2

    def __init__(self, alternativeSize: int, size: int, dataMapProvider: IDataMapProvider):
        super().__init__(SpellShapeEnum.U, alternativeSize, size, dataMapProvider)
        self.radius = size
        self._minRadius = alternativeSize

    @property
    def radius(self) -> int:
        return self._radius

    @property
    def minRadius(self) -> int:
        return self._minRadius

    @property
    def surface(self) -> int:
        return self._radius * 2 + 1

    def getCells(self, cellId: int = 0) -> list[int]:
        i: int = 0
        cells = list[int]()
        origin = MapPoint.fromCellId(cellId)
        x = origin.x
        y = origin.y
        if self._minRadius == 0:
            cells.append(cellId)
        for i in range(1, self._radius + 1):
            if self._direction == DirectionsEnum.UP_LEFT:
                self.tryAddCell(x + i, y + i, cells)
                self.tryAddCell(x + i, y - i, cells)
            elif self._direction == DirectionsEnum.UP_RIGHT:
                self.tryAddCell(x - i, y - i, cells)
                self.tryAddCell(x + i, y - i, cells)
            elif self._direction == DirectionsEnum.DOWN_RIGHT:
                self.tryAddCell(x - i, y + i, cells)
                self.tryAddCell(x - i, y - i, cells)
            elif self._direction == DirectionsEnum.DOWN_LEFT:
                self.tryAddCell(x - i, y + i, cells)
                self.tryAddCell(x + i, y + i, cells)
        return cells
