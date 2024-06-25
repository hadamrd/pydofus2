from pydofus2.com.ankamagames.atouin.AtouinConstants import AtouinConstants
from pydofus2.com.ankamagames.atouin.data.elements.subtypes.NormalGraphicalElementData import (
    NormalGraphicalElementData,
)
from pydofus2.com.ankamagames.jerakine.data.BinaryStream import BinaryStream
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger


class AnimatedGraphicalElementData(NormalGraphicalElementData):

    def __init__(self, elementId: int, elementType: int):
        super().__init__(elementId, elementType)
        self.minDelay = 0
        self.maxDelay = 0

    def fromRaw(self, raw: BinaryStream, version: int) -> None:
        super().fromRaw(raw, version)
        if version == 4:
            self.minDelay = raw.readInt()
            # Assuming AtouinConstants.DEBUG_FILES_PARSING_ELEMENTS is a global constant
            if AtouinConstants.DEBUG_FILES_PARSING_ELEMENTS:
                Logger().debug(f"  (AnimatedGraphicalElementData) minDelay : {self.minDelay}")
            self.maxDelay = raw.readInt()
            if AtouinConstants.DEBUG_FILES_PARSING_ELEMENTS:
                Logger().debug(f"  (AnimatedGraphicalElementData) maxDelay : {self.maxDelay}")
