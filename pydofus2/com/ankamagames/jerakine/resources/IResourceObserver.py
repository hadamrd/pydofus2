from abc import ABC, abstractmethod


class IResourceObserver(ABC):

    @abstractmethod
    def onLoaded(self, uri, param2, param3):
        pass

    @abstractmethod
    def onFailed(self, uri, param2, param3):
        pass

    @abstractmethod
    def onProgress(self, uri, param2, param3):
        pass
