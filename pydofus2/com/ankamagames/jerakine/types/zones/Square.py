import math

from pydofus2.com.ankamagames.jerakine.map.IDataMapProvider import IDataMapProvider
from pydofus2.com.ankamagames.jerakine.types.zones.ZRectangle import ZRectangle
from pydofus2.com.ankamagames.jerakine.utils.display.spellZone.SpellShapeEnum import SpellShapeEnum


class Square(ZRectangle):
    def __init__(self, minRadius: int, size: int, isDiagonalFree: bool, dataMapProvider: IDataMapProvider):
        super().__init__(minRadius, size, size, isDiagonalFree, dataMapProvider)
        if isDiagonalFree:
            self._shape = SpellShapeEnum.W
        else:
            self._shape = SpellShapeEnum.G

    @property
    def length(self) -> int:
        return self._width
