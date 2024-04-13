from abc import ABC, abstractmethod

from pydofus2.com.ankamagames.atouin.resources.ResourceErrorCode import ResourceErrorCode
from pydofus2.com.ankamagames.jerakine.pools.PoolsManager import PoolsManager
from pydofus2.com.ankamagames.jerakine.resources.IResourceObserver import IResourceObserver
from pydofus2.com.ankamagames.jerakine.types.Uri import Uri


class AbstractLoaderAdapter(ABC):

    _log = Log.getLogger("AbstractLoaderAdapter")
    MEMORY_LOG = {}

    def __init__(self):
        self._ldr = PoolableLoader()
        self._observer = IResourceObserver()
        self._uri = Uri()
        self._dispatchProgress = False
        AbstractLoaderAdapter.MEMORY_LOG[self] = 1

    def loadDirectly(self, uri, path, observer, dispatchProgress):
        if self._ldr:
            raise Exception("A single adapter can't handle two simultaneous loadings.")
        self._observer = observer
        self._uri = uri
        self._dispatchProgress = dispatchProgress
        self.prepareLoader()
        self._ldr.load((path if path[0:2] != "//" else "file://") + path, uri.loaderContext)

    def loadFromData(self, uri, data, observer, dispatchProgress):
        if self._ldr:
            raise Exception("A single adapter can't handle two simultaneous loadings.")
        self._observer = observer
        self._uri = uri
        self._dispatchProgress = dispatchProgress
        # self.prepareLoader()
        # self._ldr.loadBytes(data, self._uri.loaderContext)

    def free(self):
        self.releaseLoader()
        self._observer = None
        self._uri = None

    @abstractmethod
    def getResource(self, ldr):
        raise NotImplementedError("This method should be overrided.")

    @abstractmethod
    def getResourceType(self):
        raise NotImplementedError("This method should be overrided.")

    def prepareLoader(self):
        self._ldr = PoolsManager().getLoadersPool().checkOut()
        self._ldr.contentLoaderInfo.addEventListener("complete", self.onInit)
        self._ldr.contentLoaderInfo.addEventListener("ioError", self.onError)
        if self._dispatchProgress:
            self._ldr.contentLoaderInfo.addEventListener("progress", self.onProgress)

    def releaseLoader(self):
        if self._ldr:
            self._ldr.close()
            self._ldr.contentLoaderInfo.removeEventListener("complete", self.onInit)
            self._ldr.contentLoaderInfo.removeEventListener("ioError", self.onError)
            if self._dispatchProgress:
                self._ldr.contentLoaderInfo.removeEventListener("progress", self.onProgress)
            if self._ldr.loadCompleted:
                PoolsManager().getLoadersPool().checkIn(self._ldr)
            else:
                self._ldr.delayedCheckIn()

    def init(self, ldr):
        res = self.getResource(ldr)
        self.releaseLoader()
        self._observer.onLoaded(self._uri, self.getResourceType(), res)

    def onInit(self, e):
        self._ldr.loadCompleted = True
        self.init(e.target)

    def onError(self, e):
        self._ldr.loadCompleted = True
        self.releaseLoader()
        self._observer.onFailed(self._uri, e.text, ResourceErrorCode.RESOURCE_NOT_FOUND)

    def onProgress(self, e):
        self._observer.onProgress(self._uri, e.bytesLoaded, e.bytesTotal)
