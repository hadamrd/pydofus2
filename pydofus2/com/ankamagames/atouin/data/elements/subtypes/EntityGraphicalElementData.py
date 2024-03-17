from pydofus2.com.ankamagames.atouin.AtouinConstants import AtouinConstants
from pydofus2.com.ankamagames.atouin.data.elements.GraphicalElementData import \
    GraphicalElementData
from pydofus2.com.ankamagames.jerakine.data.BinaryStream import BinaryStream
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger


class EntityGraphicalElementData(GraphicalElementData):

    def __init__(self, elementId: int, elementType: int):
        super().__init__(elementId, elementType)
        self.entityLook = ''
        self.horizontalSymmetry = False
        self.playAnimation = False
        self.playAnimStatic = False
        self.minDelay = 0
        self.maxDelay = 0

    def fromRaw(self, raw: BinaryStream, version: int) -> None:
        entityLookLength = raw.readInt()
        self.entityLook = raw.readUTFBytes(entityLookLength)
        if AtouinConstants.DEBUG_FILES_PARSING_ELEMENTS:
            Logger().debug(f"  (EntityGraphicalElementData) Entity look : {self.entityLook}")
        self.horizontalSymmetry = raw.readbool()
        if AtouinConstants.DEBUG_FILES_PARSING_ELEMENTS:
            Logger().debug(f"  (EntityGraphicalElementData) Element horizontals symmetry : {self.horizontalSymmetry}")
        if version >= 7:
            self.playAnimation = raw.readbool()
            if AtouinConstants.DEBUG_FILES_PARSING_ELEMENTS:
                Logger().debug(f"  (EntityGraphicalElementData) playAnimation : {self.playAnimation}")
        if version >= 6:
            self.playAnimStatic = raw.readbool()
            if AtouinConstants.DEBUG_FILES_PARSING_ELEMENTS:
                Logger().debug(f"  (EntityGraphicalElementData) playAnimStatic : {self.playAnimStatic}")
        if version >= 5:
            self.minDelay = raw.readInt()
            if AtouinConstants.DEBUG_FILES_PARSING_ELEMENTS:
                Logger().debug(f"  (EntityGraphicalElementData) minDelay : {self.minDelay}")
            self.maxDelay = raw.readInt()
            if AtouinConstants.DEBUG_FILES_PARSING_ELEMENTS:
                Logger().debug(f"  (EntityGraphicalElementData) maxDelay : {self.maxDelay}")
