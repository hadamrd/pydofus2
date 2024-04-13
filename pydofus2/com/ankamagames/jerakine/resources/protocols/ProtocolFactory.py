from typing import Dict, Type

from pydofus2.com.ankamagames.jerakine.resources.protocols.impl.FileProtocol import FileProtocol
from pydofus2.com.ankamagames.jerakine.resources.protocols.impl.HttpProtocol import HttpProtocol
from pydofus2.com.ankamagames.jerakine.resources.protocols.impl.PakProtocol import PakProtocol
from pydofus2.com.ankamagames.jerakine.resources.protocols.impl.PakProtocol2 import PakProtocol2
from pydofus2.com.ankamagames.jerakine.resources.protocols.impl.ZipProtocol import ZipProtocol
from pydofus2.com.ankamagames.jerakine.resources.protocols.IProtocol import IProtocol
from pydofus2.com.ankamagames.jerakine.resources.ResourceError import ResourceError
from pydofus2.com.ankamagames.jerakine.types.Uri import Uri


class ProtocolFactory:
    _customProtocols: Dict[str, Type[IProtocol]] = {}

    @staticmethod
    def getProtocol(uri: Uri) -> IProtocol:
        customProtocol = ProtocolFactory._customProtocols.get(uri.protocol)
        if customProtocol:
            cp = customProtocol()
            if not isinstance(cp, IProtocol):
                raise ResourceError(
                    f"Registered custom protocol for extension {uri.protocol} isn't an IProtocol class."
                )
            return cp
        if uri.protocol == "http" or uri.protocol == "https":
            return HttpProtocol()
        elif uri.protocol == "file":
            return FileProtocol()
        elif uri.protocol == "zip":
            return ZipProtocol()
        elif uri.protocol in ["pak", "pak2", "d2p"]:
            return PakProtocol2()
        elif uri.protocol == "d2pOld":
            return PakProtocol()
        else:
            raise ValueError(f"Unknown protocol '{uri.protocol}' in the URI '{uri}'.")

    @staticmethod
    def addProtocol(protocolName: str, protocolClass: Type[IProtocol]) -> None:
        ProtocolFactory._customProtocols[protocolName] = protocolClass

    @staticmethod
    def removeProtocol(protocolName: str) -> None:
        del ProtocolFactory._customProtocols[protocolName]
