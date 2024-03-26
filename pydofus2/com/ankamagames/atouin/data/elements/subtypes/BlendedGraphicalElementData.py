from pydofus2.com.ankamagames.atouin.AtouinConstants import AtouinConstants
from pydofus2.com.ankamagames.atouin.data.elements.subtypes.NormalGraphicalElementData import \
    NormalGraphicalElementData
from pydofus2.com.ankamagames.jerakine.data.BinaryStream import BinaryStream
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger


class BlendedGraphicalElementData(NormalGraphicalElementData):

    def __init__(self, elementId: int, elementType: int):
        super().__init__(elementId, elementType)
        self.blendMode = ""

    def fromRaw(self, raw: BinaryStream, version: int) -> None:
        super().fromRaw(raw, version)
        blendModeLength = raw.readInt()
        self.blendMode = raw.readUTFBytes(blendModeLength)
        if AtouinConstants.DEBUG_FILES_PARSING_ELEMENTS:
            Logger().debug(f"  (BlendedGraphicalElementData) BlendMode : {self.blendMode}")
