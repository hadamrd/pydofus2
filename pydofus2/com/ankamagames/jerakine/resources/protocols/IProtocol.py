from abc import ABC, abstractmethod

from pydofus2.com.ankamagames.jerakine.newCache.ICache import ICache
from pydofus2.com.ankamagames.jerakine.pools.Poolable import Poolable
from pydofus2.com.ankamagames.jerakine.resources.IResourceObserver import IResourceObserver
from pydofus2.com.ankamagames.jerakine.types.Uri import Uri


class IProtocol(Poolable, ABC):
    @abstractmethod
    def load(
        self,
        uri: Uri,
        observer: IResourceObserver,
        dispatchProgress: bool,
        cache: ICache,
        forcedAdapter: type,
        singleFile: bool,
    ) -> None:
        pass

    @abstractmethod
    def cancel(self) -> None:
        pass
