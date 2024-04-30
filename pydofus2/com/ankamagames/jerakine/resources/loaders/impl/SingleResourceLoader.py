from typing import Any

from pydofus2.com.ankamagames.jerakine.newCache.ICache import ICache
from pydofus2.com.ankamagames.jerakine.resources.events.ResourceEvent import ResourceEvent
from pydofus2.com.ankamagames.jerakine.resources.IResourceObserver import IResourceObserver
from pydofus2.com.ankamagames.jerakine.resources.loaders.AbstractResourceLoader import AbstractResourceLoader
from pydofus2.com.ankamagames.jerakine.resources.loaders.IResourceLoader import IResourceLoader
from pydofus2.com.ankamagames.jerakine.resources.protocols.IProtocol import IProtocol
from pydofus2.com.ankamagames.jerakine.resources.protocols.ProtocolFactory import ProtocolFactory
from pydofus2.com.ankamagames.jerakine.types.Uri import Uri


class SingleResourceLoader(AbstractResourceLoader, IResourceLoader, IResourceObserver):
    def __init__(self):
        super().__init__()
        self._uri: Uri = None
        self._protocol: IProtocol = None

    def load(self, uri: Uri, cache: ICache = None, forcedAdapter: Any = None, singleFile: bool = False) -> None:
        if self._uri is not None:
            raise RuntimeError("A single ressource loader can't handle more than one load at a time.")
        if uri is None:
            raise ValueError("Can't load a null uri.")
        if not isinstance(uri, Uri):
            raise ValueError("Can't load an array of URIs when using a LOADER_SINGLE loader.")
        self._uri = uri
        self._cache = cache
        self._completed = False
        self._filesTotal = 1
        if not self.checkCache(self._uri):
            self._protocol = ProtocolFactory.getProtocol(self._uri)
            self._protocol.load(
                self._uri, self, self.hasListener(ResourceEvent.PROGRESS), self._cache, forcedAdapter, singleFile
            )

    def cancel(self) -> None:
        super().cancel()
        if self._protocol:
            self._protocol.cancel()
            self._protocol = None
        self._uri = None

    def onLoaded(self, uri: Uri, resourceType: int, resource: Any) -> None:
        super().onLoaded(uri, resourceType, resource)
        self._protocol = None

    def onFailed(self, uri: Uri, errorMsg: str, errorCode: int) -> None:
        super().onFailed(uri, errorMsg, errorCode)
        self._protocol = None
