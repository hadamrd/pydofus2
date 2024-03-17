import threading
from typing import Any, Dict, List, Union

from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.newCache.ICache import ICache
from pydofus2.com.ankamagames.jerakine.resources.events.ResourceEvent import \
    ResourceEvent
from pydofus2.com.ankamagames.jerakine.resources.IResourceObserver import \
    IResourceObserver
from pydofus2.com.ankamagames.jerakine.resources.loaders.AbstractResourceLoader import \
    AbstractResourceLoader
from pydofus2.com.ankamagames.jerakine.resources.loaders.IResourceLoader import \
    IResourceLoader
from pydofus2.com.ankamagames.jerakine.resources.protocols.IProtocol import \
    IProtocol
from pydofus2.com.ankamagames.jerakine.resources.protocols.ProtocolFactory import \
    ProtocolFactory
from pydofus2.com.ankamagames.jerakine.types.Uri import Uri


class ParallelResourceLoader(AbstractResourceLoader, IResourceLoader, IResourceObserver):
    def __init__(self, maxParallel: int):
        super().__init__()
        self._maxParallel = maxParallel
        self._uris = []
        self._currentlyLoading = 0
        self._loadDictionary = {}
        self._loadLock = threading.RLock()

    def load(self, uris: Union[Uri, List[Uri]], cache: ICache = None, forcedAdapter: Any = None, singleFile: bool = False) -> None:
        newUris = [uris] if isinstance(uris, Uri) else uris
        mustStartLoading = False

        with self._loadLock:
            if self._uris:
                self._filesTotal -= len(self._uris)
                self._uris.extend([{"uri": uri, "forcedAdapter": forcedAdapter, "singleFile": singleFile} for uri in newUris])
                if self._currentlyLoading == 0:
                    mustStartLoading = True
            else:
                self._uris = [{"uri": uri, "forcedAdapter": forcedAdapter, "singleFile": singleFile} for uri in newUris]
                mustStartLoading = True

            self._cache = cache
            self._completed = False
            self._filesTotal += len(self._uris)

        if mustStartLoading:
            self.loadNextUris()

    def cancel(self) -> None:
        super().cancel()
        with self._loadLock:
            for p in self._loadDictionary.values():
                if p:
                    p.free()
                    p.cancel()
            self._loadDictionary = {}
            self._currentlyLoading = 0
            self._uris = []

    def loadNextUris(self) -> None:
        if len(self._uris) == 0:
            return

        with self._loadLock:
            self._currentlyLoading = min(self._maxParallel, len(self._uris))
            starterLoop = self._currentlyLoading

            for i in range(starterLoop):
                loadData = self._uris.pop(0)
                if not self.checkCache(loadData["uri"]):
                    p = ProtocolFactory.getProtocol(loadData["uri"])
                    self._loadDictionary[loadData["uri"]] = p
                    self.loadUriWorker(p, loadData)
                else:
                    self.decrementLoads()

    def loadUriWorker(self, protocol: IProtocol, loadData: Dict) -> None:
        uri = loadData["uri"]
        forcedAdapter = loadData["forcedAdapter"]
        singleFile = loadData["singleFile"]
        protocol.load(uri, self, self.hasListener(ResourceEvent.PROGRESS), self._cache, forcedAdapter, singleFile)

    def decrementLoads(self) -> None:
        with self._loadLock:
            self._currentlyLoading -= 1
            if self._currentlyLoading == 0:
                self.loadNextUris()

    def onLoaded(self, uri: Uri, resourceType: int, resource: Any) -> None:
        Logger().debug(f"Resource : {uri.toFile()} loaded")
        super().onLoaded(uri, resourceType, resource)
        with self._loadLock:
            del self._loadDictionary[uri]
            self.decrementLoads()

    def onFailed(self, uri: Uri, errorMsg: str, errorCode: int) -> None:
        super().onFailed(uri, errorMsg, errorCode)
        with self._loadLock:
            del self._loadDictionary[uri]
            self.decrementLoads()
