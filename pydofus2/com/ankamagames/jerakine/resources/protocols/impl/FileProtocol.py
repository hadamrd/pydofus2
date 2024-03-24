import platform
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydofus2.com.ankamagames.dofus import Constants
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.newCache.ICache import ICache
from pydofus2.com.ankamagames.jerakine.resources.IResourceObserver import \
    IResourceObserver
from pydofus2.com.ankamagames.jerakine.resources.protocols.AbstractFileProtocol import \
    AbstractFileProtocol
from pydofus2.com.ankamagames.jerakine.types.Uri import Uri


class FileProtocol(AbstractFileProtocol):
    localDirectory: Optional[str] = None
    
    def __init__(self):
        self.singleFileObserver = None
        self.loadingFile: Dict[str, List[IResourceObserver]] = {}
        super().__init__()

    def load(self, uri: Uri, observer: IResourceObserver, dispatchProgress: bool, cache: ICache,
             forcedAdapter: Optional[type] = None, singleFile: bool = False) -> None:
        url = ""
        if singleFile and (uri.fileType != "swf" or not uri.subPath or len(uri.subPath) == 0):
            self.singleFileObserver = observer
            self.loadDirectly(uri, self, dispatchProgress, forcedAdapter)
        else:
            url = self.getUrl(uri)
            if url in self.loadingFile:
                self.loadingFile[url].append(observer)
            else:
                self.loadingFile[url] = [observer]
                self.loadDirectly(uri, self, dispatchProgress, forcedAdapter)

    def loadDirectly(self, uri: Uri, observer: IResourceObserver, dispatchProgress: bool, forcedAdapter: Optional[type]) -> None:
        self.getAdapter(uri, forcedAdapter)
        self.adapter.loadDirectly(uri, self.extractPath(uri.path), observer, dispatchProgress)

    def extractPath(self, path_str: str) -> str:
        absoluteFile = Path(path_str)
        if not absoluteFile.is_absolute():
            path =  Constants.DOFUS_HOME / absoluteFile
        absoluteFile = path.resolve()
        path_str = str(absoluteFile).replace("file:///", "")

        if "\\\\" in path_str:
            path_str = "file://" + path_str[path_str.index("\\\\"):]

        if FileProtocol.localDirectory is not None and path_str.startswith("./"):
            path_str = str(Path(FileProtocol.localDirectory) / path_str[2:])

        if platform.system() != "Windows" and Path(path_str).is_absolute() and not path_str.startswith("//"):
            path_str = "/" + path_str

        return path_str

    def onLoaded(self, uri: Uri, resourceType: int, resource: Any) -> None:
        url = self.getUrl(uri)
        waiting = self.loadingFile.get(url, [])
        self.loadingFile.pop(url, None)

        if self.singleFileObserver:
            self.singleFileObserver.onLoaded(uri, resourceType, resource)
            self.singleFileObserver = None
        else:
            for observer in waiting:
                observer.onLoaded(uri, resourceType, resource)

    def onFailed(self, uri: Uri, errorMsg: str, errorCode: int) -> None:
        url = self.getUrl(uri)
        waiting = self.loadingFile.get(url, [])
        self.loadingFile.pop(url, None)

        Logger().warn("onFailed " + str(uri))

        if self.singleFileObserver:
            self.singleFileObserver.onFailed(uri, errorMsg, errorCode)
            self.singleFileObserver = None
        else:
            for observer in waiting:
                observer.onFailed(uri, errorMsg, errorCode)

    def onProgress(self, uri: Uri, bytesLoaded: int, bytesTotal: int) -> None:
        url = self.getUrl(uri)
        waiting = self.loadingFile.get(url, [])
        self.loadingFile.pop(url, None)

        if self.singleFileObserver:
            self.singleFileObserver.onProgress(uri, bytesLoaded, bytesTotal)
            self.singleFileObserver = None
        else:
            for observer in waiting:
                observer.onProgress(uri, bytesLoaded, bytesTotal)
