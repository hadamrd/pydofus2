from com.ankamagames.atouin.AtouinConstants import AtouinConstants
from com.ankamagames.atouin.data.map.Cell import Cell
from com.ankamagames.atouin.data.map.elements.BasicElement import BasicElement
from com.ankamagames.atouin.enums.ElementTypesEnum import ElementTypesEnum
from com.ankamagames.jerakine.logger.Logger import Logger
from com.ankamagames.jerakine.network.CustomDataWrapper import ByteArray
from com.ankamagames.jerakine.types.ColorMultiplicator import ColorMultiplicator
from com.ankamagames.jerakine.types.positions.Point import Point

logger = Logger(__name__)


class GraphicalElement(BasicElement):

    elementId: int

    finalTeint: ColorMultiplicator

    pixelOffset: Point

    altitude: int

    identifier: int

    def __init__(self, cell: Cell):
        super().__init__(cell)

    @property
    def elementType(self) -> ElementTypesEnum:
        return ElementTypesEnum.GRAPHICAL

    @property
    def colorMultiplicator(self) -> ColorMultiplicator:
        return self.finalTeint

    def calculateFinalTeint(
        self,
        rHue: float,
        gHue: float,
        bHue: float,
        rShadow: float,
        gShadow: float,
        bShadow: float,
    ) -> None:
        r: float = ColorMultiplicator.clamp((rHue + rShadow + 128) * 2, 0, 512)
        g: float = ColorMultiplicator.clamp((gHue + gShadow + 128) * 2, 0, 512)
        b: float = ColorMultiplicator.clamp((bHue + bShadow + 128) * 2, 0, 512)
        self.finalTeint = ColorMultiplicator(r, g, b, True)

    def fromRaw(self, raw: ByteArray, mapVersion: int) -> None:
        self.subFromRaw(raw, mapVersion)
        self.identifier = raw.readUnsignedInt()
        if AtouinConstants.DEBUG_FILES_PARSING_ELEMENTS:
            logger.debug("      (GraphicalElement) Identifier : " + str(self.identifier))

    def subFromRaw(self, raw: ByteArray, mapVersion: int) -> None:
        self.elementId = raw.readUnsignedInt()
        if AtouinConstants.DEBUG_FILES_PARSING_ELEMENTS:
            logger.debug("      (GraphicalElement) Element id : " + str(self.elementId))
        self.calculateFinalTeint(
            raw.readByte(),
            raw.readByte(),
            raw.readByte(),
            raw.readByte(),
            raw.readByte(),
            raw.readByte(),
        )
        if AtouinConstants.DEBUG_FILES_PARSING_ELEMENTS:
            logger.debug("      (GraphicalElement) Teint : " + str(self.finalTeint))
        self.pixelOffset = Point()
        if mapVersion <= 4:
            self.pixelOffset.x = raw.readByte() * AtouinConstants.CELL_HALF_WIDTH
            self.pixelOffset.y = raw.readByte() * AtouinConstants.CELL_HALF_HEIGHT
        else:
            self.pixelOffset.x = raw.readShort()
            self.pixelOffset.y = raw.readShort()
        if AtouinConstants.DEBUG_FILES_PARSING_ELEMENTS:
            logger.debug(
                "      (GraphicalElement) Pixel Offset : ("
                + str(self.pixelOffset.x)
                + ""
                + str(self.pixelOffset.y)
                + ")"
            )
        self.altitude = raw.readByte()
        if AtouinConstants.DEBUG_FILES_PARSING_ELEMENTS:
            logger.debug("      (GraphicalElement) Altitude : " + str(self.altitude))
