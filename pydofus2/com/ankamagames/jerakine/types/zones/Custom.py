from pydofus2.com.ankamagames.jerakine.map.IDataMapProvider import IDataMapProvider
from pydofus2.com.ankamagames.jerakine.types.zones.DisplayZone import DisplayZone
from pydofus2.com.ankamagames.jerakine.utils.display.spellZone.SpellShapeEnum import SpellShapeEnum


class Custom(DisplayZone):

    _cells: list[int]

    def __init__(self, cells: list[int], dataMapProvider:IDataMapProvider=None):
        super().__init__(SpellShapeEnum.UNKNOWN, 0, 0, dataMapProvider)
        self._cells = cells

    @property
    def surface(self) -> int:
        return len(self._cells)

    def getCells(self, cellId: int = 0) -> list[int]:
        return self._cells
