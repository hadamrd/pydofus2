from PyQt5.QtCore import QObject, pyqtSignal

from pydofus2.com.ankamagames.jerakine.newCache.ICache import ICache
from pydofus2.com.ankamagames.jerakine.resources.CacheableResource import CacheableResource
from pydofus2.com.ankamagames.jerakine.resources.IResourceObserver import IResourceObserver
from pydofus2.com.ankamagames.jerakine.types.Uri import Uri


class AbstractResourceLoader(IResourceObserver, QObject):
    RES_CACHE_PREFIX = "RES_"
    resourceLoaded = pyqtSignal(Uri, int, object)
    loadingProgress = pyqtSignal(Uri, int, int)
    loadingComplete = pyqtSignal(int, int)
    loadFailed = pyqtSignal(Uri, str, int)

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
        self.resourceLoaded.emit(uri, resourceType, resource)
        self.loadingProgress.emit(uri, self._filesTotal, self._filesLoaded)
        if self._filesLoaded == self._filesTotal:
            self.dispatchComplete()

    def dispatchFailure(self, uri: Uri, errorMsg: str, errorCode: int):
        if self._filesTotal == 0:
            return
        self._filesLoaded += 1
        self.loadFailed.emit(uri, errorMsg, errorCode)
        if self._filesLoaded == self._filesTotal:
            self.dispatchComplete()

    def dispatchComplete(self):
        if not self._completed:
            self._completed = True
            self.loadingComplete.emit(self._filesTotal, self._filesLoaded)

    def onLoaded(self, uri: Uri, resourceType: int, resource):
        self.dispatchSuccess(uri, resourceType, resource)

    def onFailed(self, uri: Uri, errorMsg: str, errorCode: int):
        self.dispatchFailure(uri, errorMsg, errorCode)

    def onProgress(self, uri: Uri, qtyLoaded: int, qtyTotal: int):
        self.loadingProgress.emit(uri, qtyLoaded, qtyTotal)
