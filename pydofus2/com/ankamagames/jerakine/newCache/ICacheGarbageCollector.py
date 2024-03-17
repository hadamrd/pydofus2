from typing import Any

from pydofus2.com.ankamagames.jerakine.newCache.impl.Cache import Cache


class ICacheGarbageCollector:
    @property
    def cache(self) -> Cache:
        raise NotImplementedError()

    @cache.setter
    def cache(param1: Cache) -> None:
        raise NotImplementedError()

    def used(param1: Any) -> None:
        raise NotImplementedError()

    def purge(param1: int) -> None:
        raise NotImplementedError()
