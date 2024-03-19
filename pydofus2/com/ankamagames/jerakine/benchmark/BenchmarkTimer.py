import threading
from time import perf_counter
from types import FunctionType

from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger

lock = threading.Lock()


class BenchmarkTimer(threading.Thread):
    _createdTimers = dict[str, list["BenchmarkTimer"]]()
    _timers_count = 0
    _started_timers_count = 0

    def __init__(self, interval: int, function: FunctionType, args=None, kwargs=None):
        super().__init__()
        self.interval = interval
        self.function = function
        self.callerName = function.__name__
        self.parent = threading.current_thread()
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self.finished = threading.Event()
        self.startedTime = None
        BenchmarkTimer._timers_count += 1
        with lock:
            if self.parent.name not in BenchmarkTimer._createdTimers:
                BenchmarkTimer._createdTimers[self.parent.name] = []
            BenchmarkTimer._createdTimers[self.parent.name].append(self)
        self.name = self.parent.name

    def printUnstoppedTimers(self) -> None:
        for timer in BenchmarkTimer._createdTimers:
            Logger().info(f"{timer.name} is still running")
        Logger().info(f"Total unstopped Timers: {len(BenchmarkTimer._createdTimers)}")

    def start(self) -> None:
        BenchmarkTimer._started_timers_count += 1
        self.startedTime = perf_counter()
        self.finished.clear()
        super().start()
    
    def debugData(self):
        sumAllTimers = sum([len(timers) for timers in BenchmarkTimer._createdTimers.values()])
        Logger().info(f"{self.callerName} in timer, Total Timers in all threads: {sumAllTimers}")

    def remainingTime(self) -> int:
        return self.interval - (perf_counter() - self.startedTime)

    def cancel(self) -> None:
        self.finished.set()

    @classmethod
    def reset(cls) -> None:
        thname = threading.current_thread().name
        if thname in cls._createdTimers:
            while cls._createdTimers[thname]:
                timer = cls._createdTimers[thname].pop()
                if timer:
                    timer.cancel()
        Logger().debug("BenchmarTimer reseted")

    def run(self):
        if not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)
        self.finished.set()
        if self in BenchmarkTimer._createdTimers[self.parent.name]:
            BenchmarkTimer._createdTimers[self.parent.name].remove(self)
        BenchmarkTimer._started_timers_count -= 1
        BenchmarkTimer._timers_count -= 1
