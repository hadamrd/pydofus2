import math

from pydofus2.com.ankamagames.jerakine.map.IDataMapProvider import \
    IDataMapProvider
from pydofus2.com.ankamagames.jerakine.types.zones.ZRectangle import ZRectangle


class Square(ZRectangle):
    def __init__(self, nMinRadius: int, nRadius: int, dataMapProvider: IDataMapProvider):
        super().__init__(nMinRadius, nRadius, nRadius, dataMapProvider)

    @property
    def surface(self) -> int:
        return math.pow(self.radius * 2 + 1, 2)
