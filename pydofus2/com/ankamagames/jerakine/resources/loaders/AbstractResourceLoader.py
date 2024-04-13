from pydofus2.com.ankamagames.berilia.managers.EventsHandler import EventsHandler
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.newCache.ICache import ICache
from pydofus2.com.ankamagames.jerakine.resources.CacheableResource import CacheableResource
from pydofus2.com.ankamagames.jerakine.resources.events.ResourceEvent import ResourceEvent
from pydofus2.com.ankamagames.jerakine.resources.IResourceObserver import IResourceObserver
from pydofus2.com.ankamagames.jerakine.types.Uri import Uri


class AbstractResourceLoader(IResourceObserver, EventsHandler):

    _log = None
    MEMORY_TEST = {}
    RES_CACHE_PREFIX = "RES_"

    def __init__(self):
        self._cache: ICache = None
        self._completed = False
        self._filesLoaded = 0
        self._filesTotal = 0
        super().__init__()

    def checkCache(self, uri: Uri) -> bool:
        cr = self.getCachedValue(uri)
        if cr is not None:
            self.dispatchSuccess(uri, cr.resourceType, cr.resource)
            return True
        return False

    def getCachedValue(self, uri: Uri) -> CacheableResource:
        if uri.protocol == "pak" or uri.fileType != "swf" or not uri.subPath:
            resourceUrl = self.RES_CACHE_PREFIX + uri.toSum()
        else:
            resourceUrl = self.RES_CACHE_PREFIX + Uri(uri.path).toSum()
        if self._cache and self._cache.contains(resourceUrl):
            cr = self._cache.peek(resourceUrl)
            return cr
        return None

    def isInCache(self, uri: Uri) -> bool:
        return self.getCachedValue(uri) is not None

    def cancel(self) -> None:
        self._filesTotal = 0
        self._filesLoaded = 0
        self._completed = False
        self._cache = None

    def dispatchSuccess(self, uri: Uri, resourceType: int, resource):
        if uri.fileType != "swf" or not uri.subPath or len(uri.subPath) == 0:
            resourceUrl = self.RES_CACHE_PREFIX + uri.toSum()
        else:
            resourceUrl = self.RES_CACHE_PREFIX + Uri(uri.path).toSum()
        if self._cache and not self._cache.contains(resourceUrl):
            cr = CacheableResource(resourceType, resource)
            self._cache.store(resourceUrl, cr)
        self._filesLoaded += 1
        self.send(ResourceEvent.LOADED, uri, resourceType, resource)
        self.send(ResourceEvent.LOADER_PROGRESS, uri, self._filesTotal, self._filesLoaded)
        if self._filesLoaded == self._filesTotal:
            self.dispatchComplete()

    def dispatchFailure(self, uri: Uri, errorMsg: str, errorCode: int):
        if self._filesTotal == 0:
            return
        self._filesLoaded += 1
        if self.hasListener(ResourceEvent.ERROR):
            self.send(ResourceEvent.ERROR, uri, errorMsg, errorCode)
        else:
            Logger().error(
                "[Error code " + str(hex(errorCode)) + "] Unable to load resource " + str(uri) + ": " + errorMsg
            )
        if self._filesLoaded == self._filesTotal:
            self.dispatchComplete()

    def dispatchComplete(self):
        if not self._completed:
            self._completed = True
            self.send(ResourceEvent.LOADER_COMPLETE, self._filesTotal, self._filesLoaded)

    def onLoaded(self, uri: Uri, resourceType: int, resource):
        self.dispatchSuccess(uri, resourceType, resource)

    def onFailed(self, uri: Uri, errorMsg: str, errorCode: int):
        self.dispatchFailure(uri, errorMsg, errorCode)

    def onProgress(self, uri: Uri, bytesLoaded: int, bytesTotal: int):
        self.send(ResourceEvent.PROGRESS, uri, bytesLoaded, bytesTotal)
