from pydofus2.com.ankamagames.atouin.AtouinConstants import AtouinConstants
from pydofus2.com.ankamagames.atouin.data.elements.GraphicalElementData import GraphicalElementData
from pydofus2.com.ankamagames.jerakine.data.BinaryStream import BinaryStream
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger


class ParticlesGraphicalElementData(GraphicalElementData):

    def __init__(self, elementId: int, elementType: int):
        super().__init__(elementId, elementType)
        self.scriptId = 0

    def fromRaw(self, raw: BinaryStream, version: int) -> None:
        self.scriptId = raw.readShort()
        if AtouinConstants.DEBUG_FILES_PARSING_ELEMENTS:
            Logger().debug(f"  (ParticlesGraphicalElementData) Script id : {self.scriptId}")
