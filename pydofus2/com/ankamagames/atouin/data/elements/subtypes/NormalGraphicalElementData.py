from pydofus2.com.ankamagames.atouin.AtouinConstants import AtouinConstants
from pydofus2.com.ankamagames.atouin.data.elements.GraphicalElementData import GraphicalElementData
from pydofus2.com.ankamagames.jerakine.data.BinaryStream import BinaryStream
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.flash.geom.Point import Point


class NormalGraphicalElementData(GraphicalElementData):

    def __init__(self, elementId: int, elementType: int):
        super().__init__(elementId, elementType)
        self.gfxId: int = None
        self.height: int = None
        self.horizontalSymmetry: bool = None
        self.origin: Point = None
        self.size: Point = None

    def fromRaw(self, raw: BinaryStream, version: int) -> None:
        self.gfxId = raw.readInt()
        if AtouinConstants.DEBUG_FILES_PARSING_ELEMENTS:
            Logger().debug(f"  (ElementData) Element gfx id : {self.gfxId}")
        self.height = raw.readByte()
        if AtouinConstants.DEBUG_FILES_PARSING_ELEMENTS:
            Logger().debug(f"  (ElementData) Element height : {self.height}")
        self.horizontalSymmetry = raw.readbool()
        if AtouinConstants.DEBUG_FILES_PARSING_ELEMENTS:
            Logger().debug(f"  (ElementData) Element horizontals symmetry : {self.horizontalSymmetry}")
        self.origin = Point(raw.readShort(), raw.readShort())
        if AtouinConstants.DEBUG_FILES_PARSING_ELEMENTS:
            Logger().debug(f"  (ElementData) Origin : ({self.origin.x};{self.origin.y})")
        self.size = Point(raw.readShort(), raw.readShort())
        if AtouinConstants.DEBUG_FILES_PARSING_ELEMENTS:
            Logger().debug(f"  (ElementData) Size : ({self.size.x};{self.size.y})")
