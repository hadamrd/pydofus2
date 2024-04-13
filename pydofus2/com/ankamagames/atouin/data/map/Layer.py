from pydofus2.com.ankamagames.atouin.AtouinConstants import AtouinConstants
from pydofus2.com.ankamagames.atouin.data.map.elements.BasicElement import BasicElement
from pydofus2.com.ankamagames.jerakine.data.BinaryStream import BinaryStream
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger


class Layer:

    LAYER_GROUND = 0

    LAYER_ADDITIONAL_GROUND = 1

    LAYER_DECOR = 2

    LAYER_ADDITIONAL_DECOR = 3

    def __init__(self, raw, mapVersion):
        self.version = mapVersion
        self.read(raw)

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
        self.read(raw)

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
