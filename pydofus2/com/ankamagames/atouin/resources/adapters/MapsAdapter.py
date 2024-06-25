import zlib
from io import BytesIO
from typing import Optional, Union

from pydofus2.com.ankamagames.atouin.resources.AtouinResourceType import AtouinResourceType
from pydofus2.com.ankamagames.atouin.resources.ResourceErrorCode import ResourceErrorCode
from pydofus2.com.ankamagames.jerakine.data.BinaryStream import BinaryStream
from pydofus2.com.ankamagames.jerakine.resources.adapters.AbstractUrlLoaderAdapter import AbstractUrlLoaderAdapter


class MapsAdapter(AbstractUrlLoaderAdapter):

    def __init__(self):
        super().__init__()

    def getResource(self, dataFormat: str, data: Union[bytes, bytearray]) -> Optional[BinaryStream]:
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("Expected bytes or bytearray")
        ba = BinaryStream(BytesIO(data), True)
        header = ba.readByte()
        if header != ord("M"):
            ba.position = 0
            try:
                data = zlib.decompress(data)
                ba = BinaryStream(BytesIO(data), True)
            except IOError:
                self.dispatchFailure("Wrong header and non-compressed file.", ResourceErrorCode.MALFORMED_MAP_FILE)
                return None
            header = ba.readByte()
            if header != ord("M"):
                self.dispatchFailure("Wrong header file.", ResourceErrorCode.MALFORMED_MAP_FILE)
                return None
        ba.position = 0
        return ba

    def getResourceType(self) -> int:
        return AtouinResourceType.RESOURCE_MAP

    def getDataFormat(self) -> str:
        return "BINARY"
