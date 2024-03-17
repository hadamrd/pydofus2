import abc
from typing import Any

import requests

from pydofus2.com.ankamagames.jerakine.resources.IResourceObserver import \
    IResourceObserver
from pydofus2.com.ankamagames.jerakine.types.Uri import Uri


class AbstractUrlLoaderAdapter(metaclass=abc.ABCMeta):

    def __init__(self):
        self._observer = None
        self._uri = None
        self._dispatchProgress = None

    def loadDirectly(self, uri: Uri, path, observer:IResourceObserver, dispatchProgress):
        if self._observer is not None:
            raise Exception("A single adapter can't handle two simultaneous loadings.")
        self._observer = observer
        self._uri = uri
        self._dispatchProgress = dispatchProgress

        if uri.protocol == "file":
            with open(path, "rb") as file:
                self.process("BINARY", file.read())
        else:
            response = requests.get(path)
            self.process(response.content)
            
    def loadFromData(self, uri, data, observer, dispatchProgress):
        if self._observer is not None:
            raise Exception("A single adapter can't handle two simultaneous loadings.")
        self._observer = observer
        self._uri = uri
        self._dispatchProgress = dispatchProgress
        self.process(data)

    def free(self):
        self._observer = None
        self._uri = None

    def process(self, dataFormat:str, data):
        resource = self.getResource(dataFormat, data)
        self._observer.onLoaded(self._uri, self.getResourceType(), resource)
        self.free()

    def dispatchSuccess(self, dataFormat: str, data: Any) -> None:
        res = self.getResource(dataFormat, data)
        self.releaseLoader()
        self._observer.onLoaded(self._uri, self.getResourceType(), res)

    def dispatchFailure(self, errorMsg: str, errorCode: int) -> None:
        self.releaseLoader()
        self._observer.onFailed(self._uri, errorMsg, errorCode)

    def getDataFormat(self) -> str:
        return "text/plain"

    def getUri(self) -> Uri:
        return self._uri
    
    @abc.abstractmethod
    def getResource(self):
        pass
    
    @abc.abstractmethod
    def getResourceType(self):
        pass
    
    def releaseLoader(self) -> None:
        pass
