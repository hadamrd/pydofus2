from abc import ABC, abstractmethod
from typing import Any

from pydofus2.com.ankamagames.jerakine.newCache.ICache import ICache
from pydofus2.com.ankamagames.jerakine.types.Uri import Uri


class IResourceLoader(ABC):

    @abstractmethod
    def load(self, param1: Any, param2: ICache = None, param3: Any = None, param4: bool = False) -> None:
        pass

    @abstractmethod
    def cancel(self) -> None:
        pass

    @abstractmethod
    def isInCache(self, param1: Uri) -> bool:
        pass
