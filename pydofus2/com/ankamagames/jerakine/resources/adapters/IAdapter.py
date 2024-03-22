from abc import ABC, abstractmethod


class IAdapter(ABC):
    
    @abstractmethod
    def loadDirectly(self, uri, path, observer, dispatchProgress):
        pass

    @abstractmethod
    def loadFromData(self, uri, data, observer, dispatchProgress):
        pass

    @abstractmethod
    def getResourceType(self):
        pass

    # Depending on your use-case, you might want to include additional methods here related to pool management.
