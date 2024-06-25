import concurrent.futures
import threading
from typing import Any, List, Union

from pydofus2.com.ankamagames.jerakine.newCache.ICache import ICache
from pydofus2.com.ankamagames.jerakine.resources.IResourceObserver import IResourceObserver
from pydofus2.com.ankamagames.jerakine.resources.loaders.AbstractResourceLoader import AbstractResourceLoader
from pydofus2.com.ankamagames.jerakine.resources.loaders.IResourceLoader import IResourceLoader
from pydofus2.com.ankamagames.jerakine.resources.protocols.ProtocolFactory import ProtocolFactory
from pydofus2.com.ankamagames.jerakine.types.Uri import Uri


class ParallelResourceLoader(AbstractResourceLoader, IResourceLoader, IResourceObserver):
    def __init__(self, maxParallel: int):
        super().__init__()
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=maxParallel)
        self._tasksPool = {}
        self._loadLock = threading.RLock()
        self._cache = None
        self._loadingInProgress = False
        self._filesTotal = 0  # Track the total files scheduled for loading

    def load(
        self, uris: Union[Uri, List[Uri]], cache: ICache = None, forcedAdapter: Any = None, singleFile: bool = False
    ) -> None:
        uris = [uris] if isinstance(uris, Uri) else uris
        with self._loadLock:
            if not self._loadingInProgress:
                self._loadingInProgress = True  # Indicate that loading is in progress
            for uri in uris:
                if uri not in self._tasksPool:  # Avoid adding duplicate URIs
                    task = self._executor.submit(self.loadUriWorker, uri, forcedAdapter, singleFile)
                    self._tasksPool[uri] = task
                    self._filesTotal += 1  # Increment the total files counter safely within the lock

    def loadUriWorker(self, uri: Uri, forcedAdapter: Any, singleFile: bool) -> None:
        try:
            protocol = ProtocolFactory.getProtocol(uri)
            protocol.load(uri, self, self._cache, forcedAdapter, singleFile)
        except Exception as e:
            self.onFailed(uri, str(e), e.__class__.__name__)

    def cancel(self) -> None:
        super().cancel()
        with self._loadLock:
            for task in self._tasksPool.values():
                task.cancel()
            self._tasksPool.clear()
            self._filesTotal = 0  # Reset the total files counter
            self._loadingInProgress = False

    def onLoaded(self, uri: Uri, resourceType: int, resource: Any) -> None:
        super().onLoaded(uri, resourceType, resource)
        with self._loadLock:
            self._tasksPool.pop(uri, None)

    def onFailed(self, uri: Uri, errorMsg: str, errorCode: int) -> None:
        super().onFailed(uri, errorMsg, errorCode)
        with self._loadLock:
            self._tasksPool.pop(uri, None)
