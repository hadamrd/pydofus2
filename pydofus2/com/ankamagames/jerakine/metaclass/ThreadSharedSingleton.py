import threading
from typing import Any, Type, TypeVar

lock = threading.RLock()
_locks = dict[type, threading.RLock]()

T = TypeVar("T")


class ThreadSharedSingleton(type):
    _instances = dict[type, Any]()

    def __call__(cls: Type[T], *args, **kwargs) -> T:
        with lock:
            if cls not in _locks:
                _locks[cls] = threading.RLock()
        with _locks[cls]:
            if cls not in ThreadSharedSingleton._instances:
                ThreadSharedSingleton._instances[cls] = super(ThreadSharedSingleton, cls).__call__(*args, **kwargs)
        return ThreadSharedSingleton._instances[cls]

    def clear(cls):
        if cls in _locks:
            with _locks[cls]:
                if cls in cls._instances:
                    del cls._instances[cls]
