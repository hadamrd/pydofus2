from abc import ABC, abstractmethod

from pydofus2.com.ankamagames.jerakine.resources.adapters.AdapterFactory import AdapterFactory
from pydofus2.com.ankamagames.jerakine.resources.adapters.IAdapter import IAdapter
from pydofus2.com.ankamagames.jerakine.resources.IResourceObserver import IResourceObserver
from pydofus2.com.ankamagames.jerakine.types.Uri import Uri


class AbstractProtocol(ABC):
    def __init__(self):
        self._observer: IResourceObserver = None
        self._adapter: IAdapter = None

    def free(self):
        self.release()
        self._observer = None
        self._adapter = None

    def cancel(self):
        pass

    @abstractmethod
    def release(self):
        raise NotImplementedError(
            "AbstractProtocol subclasses must override the release method to free their resources."
        )

    def loadDirectly(self, uri: Uri, observer, forcedAdapter):
        self.getAdapter(uri, forcedAdapter)
        self._adapter.loadDirectly(uri, uri.path, observer)

    def loadFromData(self, uri, data, observer, forcedAdapter):
        self.getAdapter(uri, forcedAdapter)
        self._adapter.loadFromData(uri, data, observer)

    def getAdapter(self, uri, forcedAdapter):
        if forcedAdapter is None:
            self._adapter = AdapterFactory.getAdapter(uri)
        else:
            self._adapter = forcedAdapter()
