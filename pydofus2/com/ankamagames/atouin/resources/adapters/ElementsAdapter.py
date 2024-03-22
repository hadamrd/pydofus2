import tempfile
import zlib
from typing import Optional, Union

from pydofus2.com.ankamagames.atouin.data.elements.Elements import Elements
from pydofus2.com.ankamagames.atouin.resources.AtouinResourceType import \
    AtouinResourceType
from pydofus2.com.ankamagames.atouin.resources.ResourceErrorCode import \
    ResourceErrorCode
from pydofus2.com.ankamagames.jerakine.data.BinaryStream import BinaryStream
from pydofus2.com.ankamagames.jerakine.resources.adapters.AbstractUrlLoaderAdapter import \
    AbstractUrlLoaderAdapter
from pydofus2.com.ankamagames.jerakine.resources.adapters.IAdapter import \
    IAdapter


class ElementsAdapter(AbstractUrlLoaderAdapter, IAdapter):
    
    def __init__(self):
        super().__init__()

    def getResource(self, dataFormat: str, data: Union[bytes, bytearray]) -> Optional[Elements]:
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("Expected bytes or bytearray")
        try:
            ele_uncompressed = tempfile.TemporaryFile()
            ele_uncompressed.write(zlib.decompress(data))
            ele_uncompressed.seek(0)
            ba = BinaryStream(ele_uncompressed, True)
        except IOError as ioe:
            self.dispatchFailure("Wrong header and non-compressed file.", ResourceErrorCode.MALFORMED_ELE_FILE)
            return None        
        header = ba.readByte()
        if header != ord('E'):
            ba.position = 0
            header = ba.readByte()
            if header != ord('E'):
                self.dispatchFailure("Wrong header file.", ResourceErrorCode.MALFORMED_ELE_FILE)
                return None
        ba.position = 0
        Elements().fromRaw(ba)
        return Elements()

    def getResourceType(self) -> int:
        return AtouinResourceType.RESOURCE_ELEMENTS

    def getDataFormat(self) -> str:
        return "BINARY"
