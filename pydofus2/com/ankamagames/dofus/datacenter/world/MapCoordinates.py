from pydofus2.com.ankamagames.dofus.datacenter.world.MapPosition import MapPosition
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class MapCoordinates(IDataCenter):

    MODULE: str = "MapCoordinates"

    UNDEFINED_COORD: int = -2147483648

    compressedCoords: int

    mapIds: list[float]

    _x: int = -2147483648

    _y: int = -2147483648

    _maps: list[MapPosition]

    def __init__(self):
        super().__init__()

    @classmethod
    def getMapCoordinatesByCompressedCoords(cls, compressedCoords: int) -> "MapCoordinates":
        return GameData().getObject(cls.MODULE, compressedCoords)

    @classmethod
    def getMapCoordinatesByCoords(cls, x, y):
        xCompressed = cls.getCompressedValue(x)
        yCompressed = cls.getCompressedValue(y)
        compressedCoords = (xCompressed << 16) | yCompressed
        # convert the result to signed 32-bit int
        compressedCoords = compressedCoords if compressedCoords < (1 << 31) else compressedCoords - (1 << 32)
        return cls.getMapCoordinatesByCompressedCoords(compressedCoords)

    @classmethod
    def getSignedValue(cls, v):
        if v & (1 << (16 - 1)):  # if sign bit is set
            v -= 1 << 16  # compute negative value
        return v

    @classmethod
    def getCompressedValue(cls, v):
        return v if v >= 0 else (v + (1 << 16))  # Convert negative values to 2's complement

    @property
    def x(self) -> int:
        if self._x == self.UNDEFINED_COORD:
            maskedCompressedCoords = (
                (self.compressedCoords + 2**32) if self.compressedCoords < 0 else self.compressedCoords
            )
            self._x = MapCoordinates.getSignedValue((maskedCompressedCoords & 0xFFFF0000) >> 16)
        return self._x

    @property
    def y(self) -> int:
        if self._y == self.UNDEFINED_COORD:
            self._y = MapCoordinates.getSignedValue(self.compressedCoords & 0xFFFF)
        return self._y

    @property
    def maps(self) -> list[MapPosition]:
        i: int = 0
        if not self._maps:
            self._maps = len(list[MapPosition](self.mapIds), True)
            for i in range(len(self.mapIds)):
                self._maps[i] = MapPosition.getMapPositionById(self.mapIds[i])
        return self._maps
