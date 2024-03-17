from typing import Any, Dict

from pydofus2.com.ankamagames.jerakine.newCache.ICache import ICache
from pydofus2.com.ankamagames.jerakine.resources.adapters.IAdapter import \
    IAdapter
from pydofus2.com.ankamagames.jerakine.resources.IResourceObserver import \
    IResourceObserver
from pydofus2.com.ankamagames.jerakine.resources.protocols.AbstractProtocol import \
    AbstractProtocol
from pydofus2.com.ankamagames.jerakine.resources.protocols.IProtocol import \
    IProtocol
from pydofus2.com.ankamagames.jerakine.types.Uri import Uri


class AbstractFileProtocol(AbstractProtocol, IProtocol, IResourceObserver):
    _loadingFile: Dict = {}

    def __init__(self):
        super().__init__()
        self._singleFileObserver = None

    def initAdapter(self, uri: Uri, forcedAdapter: type) -> None:
        self.getAdapter(uri, forcedAdapter)

    def getUrl(self, uri: Uri) -> str:
        if uri.fileType != "swf" or not uri.subPath or len(uri.subPath) == 0:
            return uri.normalizedUri
        return uri.normalizedUriWithoutSubPath

    def release(self) -> None:
        if self._adapter:
            self._adapter.free()
        self._loadingFile = {}

    @property
    def adapter(self) -> IAdapter:
        return self._adapter

    @property
    def loadingFile(self) -> Dict:
        return self._loadingFile

    @loadingFile.setter
    def loadingFile(self, value: Dict) -> None:
        self._loadingFile = value

    def load(self, uri: Uri, observer: IResourceObserver, dispatchProgress: bool, cache: ICache,
             forcedAdapter: type, singleFile: bool) -> None:
        raise NotImplementedError("AbstractProtocol childs must override the release method in order to free their resources.")

    def onLoaded(self, uri: Uri, resourceType: int, resource: Any) -> None:
        raise NotImplementedError("AbstractProtocol childs must override the release method in order to free their resources.")

    def onFailed(self, uri: Uri, errorMsg: str, errorCode: int) -> None:
        raise NotImplementedError("AbstractProtocol childs must override the release method in order to free their resources.")

    def onProgress(self, uri: Uri, bytesLoaded: int, bytesTotal: int) -> None:
        raise NotImplementedError("AbstractProtocol childs must override the release method in order to free their resources.")

    def extractPath(self, path: str) -> str:
        raise NotImplementedError("AbstractProtocol childs must override the release method in order to free their resources.")
