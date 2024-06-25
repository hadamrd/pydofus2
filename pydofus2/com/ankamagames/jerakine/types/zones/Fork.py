from typing import List

from pydofus2.com.ankamagames.jerakine.map.IDataMapProvider import IDataMapProvider
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint
from pydofus2.com.ankamagames.jerakine.types.zones.DisplayZone import DisplayZone
from pydofus2.com.ankamagames.jerakine.utils.display.spellZone.SpellShapeEnum import SpellShapeEnum
from pydofus2.mapTools.MapDirection import MapDirection


class Fork(DisplayZone):
    def __init__(self, size: int, dataMapProvider: IDataMapProvider):
        super().__init__(SpellShapeEnum.F, 0, size, dataMapProvider)
        self._length = size + 1

    @property
    def length(self) -> int:
        return self._length

    def getSurface(self) -> int:
        return 1 + 3 * self._length

    def getCells(self, cell_id: int = 0) -> List[int]:
        origin = MapPoint.fromCellId(cell_id)
        cells = [cell_id]
        sign = -1 if self._direction == MapDirection.NORTH_WEST or self._direction == MapDirection.SOUTH_WEST else 1
        axis_flag = self._direction == MapDirection.NORTH_WEST or self._direction == MapDirection.SOUTH_EAST

        for i in range(1, self._length + 1):
            for j in range(-1, 2):
                x = 0
                y = 0
                if axis_flag:
                    x = origin.x + i * sign
                    y = origin.y + j * i
                else:
                    x = origin.x + j * i
                    y = origin.y + i * sign
                self.try_add_cell(x, y, cells)

        return cells
