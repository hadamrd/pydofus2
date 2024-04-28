import threading
from enum import Enum
from typing import Any, Generator, List, Tuple, Type, TypeVar

from pydofus2.com.ankamagames.berilia.managers.EventsHandler import Event, EventsHandler
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger

LOCK = threading.Lock()
T = TypeVar("T")


class SingletonEvent(Enum):
    THREAD_REGISTER = 0


class Singleton(type):
    _instances = dict[str, dict[type, Any]]()
    _wait_events = dict[str, dict[type, threading.Event]]()
    eventsHandler = EventsHandler()

    @staticmethod
    def threadName():
        return threading.current_thread().name

    @property
    def lightInfo(cls):
        return {thread_name: [c.__qualname__ for c in cls._instances[thread_name]] for thread_name in cls._instances}

    def __call__(cls: Type[T], *args, **kwargs) -> T:
        thread_name = Singleton.threadName()
        if thread_name not in Singleton._instances:
            Singleton._instances[thread_name] = dict()
        if cls not in cls._instances[thread_name]:
            Singleton._instances[thread_name][cls] = super(Singleton, cls).__call__(*args, **kwargs)
            Singleton.eventsHandler.send(SingletonEvent.THREAD_REGISTER, thread_name, cls)
        return Singleton._instances[thread_name][cls]

    @staticmethod
    def clearAll():
        thread_name = threading.current_thread().name
        Singleton._instances[thread_name].clear()

    def clear(cls):
        with LOCK:
            if cls in Singleton._instances[cls.threadName()]:
                del Singleton._instances[cls.threadName()][cls]
        Logger().debug(f"{cls.__name__} reset")

    def getSubs(cls: Type[T], thname=None) -> Generator[T, T, None]:
        thname = thname if thname is not None else Singleton.threadName()
        for clz in Singleton._instances[thname]:
            if issubclass(clz, cls):
                yield Singleton._instances[thname][clz]

    def clearAllChilds(cls):
        with LOCK:
            scheduledForDelete = []
            for clz in Singleton._instances[cls.threadName()]:
                if issubclass(clz, cls):
                    scheduledForDelete.append(clz)
            for clz in scheduledForDelete:
                Logger().debug(f"{clz.__name__} singleton instance cleared")
                del Singleton._instances[cls.threadName()][clz]
            scheduledForDelete.clear()

    def getInstance(cls: Type[T], thread_name: int) -> T:
        if thread_name in Singleton._instances:
            return Singleton._instances[thread_name].get(cls)

    def getInstances(cls: Type[T]) -> List[Tuple[str, T]]:
        return [
            (thd, Singleton._instances[thd][cls]) for thd in Singleton._instances if cls in Singleton._instances[thd]
        ]

    def onceThreadRegister(cls, thname: str, listener, args=[], kwargs={}, priority=0, timeout=None, ontimeout=None):
        if thname in Singleton._instances and cls in Singleton._instances[thname]:
            return listener(*args, **kwargs)

        def onThreadRegister(evt: Event, thread_name, cls):
            if thread_name == thname and cls.__name__ == cls.__name__:
                evt.listener.delete()
                listener(*args, **kwargs)

        Singleton.eventsHandler.on(SingletonEvent.THREAD_REGISTER, onThreadRegister, priority, timeout, ontimeout)

    def waitThreadRegister(cls: Type[T], thname: str, timeout: float) -> T:
        if thname in Singleton._instances and cls in Singleton._instances[thname]:
            return cls.getInstance(thname)
        waitEvt = threading.Event()
        Singleton._wait_events[thname] = waitEvt
        cls.onceThreadRegister(thname, waitEvt.set)
        if not waitEvt.wait(timeout):
            raise TimeoutError(f"wait for {cls.__name__} singleton instantiation from thread {thname} timed out!")
        return cls.getInstance(thname)

    @staticmethod
    def clearEventsWaits(thname):
        if thname in Singleton._wait_events:
            Singleton._wait_events[thname].set()
            del Singleton._wait_events[thname]
