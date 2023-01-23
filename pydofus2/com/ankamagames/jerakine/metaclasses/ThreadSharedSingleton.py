import threading
lock = threading.Lock()

class ThreadSharedSingleton(type):
    _instances = dict[type, object]()
    def __call__(cls, *args, **kwargs) -> object:
        with lock:
            if cls not in cls._instances:
                cls._instances[cls] = super(ThreadSharedSingleton, cls).__call__(*args, **kwargs)
            return cls._instances[cls]

    def clear(cls):
        cls._instances.clear()
