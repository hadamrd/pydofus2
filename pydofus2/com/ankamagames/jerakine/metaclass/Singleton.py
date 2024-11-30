import threading
from collections import defaultdict
from typing import Generator, List, Tuple, Type, TypeVar

from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger

LOCK = threading.Lock()
T = TypeVar("T")


class Singleton(type):
    __instances = defaultdict(dict)  # thread -> {class -> instance}

    @staticmethod
    def threadName():
        return threading.current_thread().name

    @property
    def lightInfo(cls):
        return {thread_name: [c.__qualname__ for c in cls.__instances[thread_name]] for thread_name in cls.__instances}

    def __call__(cls: Type[T], *args, **kwargs) -> T:
        thread_name = Singleton.threadName()
        if cls not in cls.__instances[thread_name]:
            Singleton.__instances[thread_name][cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return Singleton.__instances[thread_name][cls]

    @staticmethod
    def clearAll():
        thread_name = Singleton.threadName()
        Singleton.__instances[thread_name].clear()

    def clear(cls):
        with LOCK:
            if cls in Singleton.__instances[cls.threadName()]:
                del Singleton.__instances[cls.threadName()][cls]

    def getSubs(cls: Type[T], thname=None) -> Generator[T, T, None]:
        thname = str(thname) if thname is not None else Singleton.threadName()
        for clz in Singleton.__instances[thname]:
            if issubclass(clz, cls):
                yield Singleton.__instances[thname][clz]

    def clear_children(cls):
        with LOCK:
            to_delete = []
            for clz in Singleton.__instances[cls.threadName()]:
                if issubclass(clz, cls):
                    to_delete.append(clz)
            for clz in to_delete:
                Logger().debug(f"{clz.__name__} singleton instance cleared")
                del Singleton.__instances[cls.threadName()][clz]
            to_delete.clear()

    def getInstance(cls: Type[T], thread_name: str = None) -> T:
        if thread_name is None:
            thread_name = threading.current_thread().name
        return Singleton.__instances[str(thread_name)].get(cls)

    def getInstances(cls: Type[T]) -> List[Tuple[str, T]]:
        return [
            (thd, Singleton.__instances[thd][cls])
            for thd in Singleton.__instances
            if cls in Singleton.__instances[thd]
        ]
