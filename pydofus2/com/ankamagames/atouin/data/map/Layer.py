import math

from pydofus2.com.ankamagames.atouin.AtouinConstants import AtouinConstants
from pydofus2.com.ankamagames.atouin.data.map.elements.BasicElement import BasicElement
from pydofus2.com.ankamagames.jerakine.data.BinaryStream import BinaryStream
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.flash.geom.Point import Point


class Layer:

    LAYER_GROUND = 0

    LAYER_ADDITIONAL_GROUND = 1

    LAYER_DECOR = 2

    LAYER_ADDITIONAL_DECOR = 3

    def __init__(self, raw, mapVersion):
        self.version = mapVersion
        self.read(raw)

    def isGround(self):
        return self.layerId == self.LAYER_GROUND

    def isDecor(self):
        return self.layerId == self.LAYER_DECOR

    def read(self, raw: BinaryStream):
        if self.version >= 9:
            self.layerId = raw.readByte()
        else:
            self.layerId = raw.readInt()
        self.cellsCount = raw.readShort()
        self.cells = [LayerCell(raw, self.version) for _ in range(self.cellsCount)]


class LayerCell:
    def __init__(self, raw: BinaryStream, mapVersion):
        self.mapVersion = mapVersion
        self._cellCoords = None
        self.read(raw)

    def cellCoords(self, cellId: int) -> Point:
        if self._cellCoords is None:
            self._cellCoords = Point()
            self._cellCoords.x = cellId % AtouinConstants.MAP_WIDTH
            self._cellCoords.y = math.floor(cellId / AtouinConstants.MAP_WIDTH)
        return self._cellCoords

    def cellPixelCoords(self, cellId: int) -> Point:
        p = self.cellCoords(cellId)
        p.x = p.x * AtouinConstants.CELL_WIDTH + (AtouinConstants.CELL_HALF_WIDTH if p.y % 2 == 1 else 0)
        p.y *= AtouinConstants.CELL_HALF_HEIGHT
        return p

    @property
    def pixelCoords(self):
        return self.cellPixelCoords(self.cellId)

    def read(self, raw: BinaryStream):
        self.cellId = raw.readShort()
        self.elementsCount = raw.readShort()
        self.elements: list[BasicElement] = [None] * self.elementsCount
        for i in range(self.elementsCount):
            be = BasicElement.getElementFromType(raw.readByte(), self)
            if AtouinConstants.DEBUG_FILES_PARSING:
                Logger().debug("    (Cell) Element at index " + i + " :")
            be.fromRaw(raw, self.mapVersion)
            self.elements[i] = be
