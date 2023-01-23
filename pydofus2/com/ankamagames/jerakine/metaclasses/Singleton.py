import threading
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger


logger = Logger()
class Singleton(type):
    _instances = dict[int, dict[type, object]]()

    def threadName(cls):
        return threading.current_thread().name
    
    @property
    def lightInfo(cls):
        return {thrid: [c.__qualname__ for c in cls._instances[thrid]] for thrid in cls._instances}
    
    def __call__(cls, *args, **kwargs) -> object:
        thrid = cls.threadName()
        if thrid not in cls._instances:
            logger.info(f"New thread {thrid} want to register class {cls.__qualname__} as singleton")
            cls._instances[thrid] = dict()
        if cls not in cls._instances[thrid]:
            cls._instances[thrid][cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[thrid][cls]

    def clear(cls):
        if cls in cls._instances[cls.threadName()]:
            del cls._instances[cls.threadName()][cls]
