import threading
from collections import defaultdict
from time import perf_counter
from types import FunctionType
from typing import Optional

import pydofus2.com.ankamagames.dofus.kernel.Kernel as core
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger


class BenchmarkTimer(threading.Thread):
    _timers = defaultdict(list)
    _timers_count = 0
    _started_timers_count = 0
    logger = Logger()

    def __init__(
        self, interval: float, function: FunctionType, args: Optional[list] = None, kwargs: Optional[dict] = None
    ) -> None:
        super().__init__(daemon=True)

        self.interval = interval
        self.function = function
        self.caller_name = function.__name__
        self.parent = threading.current_thread()
        self.args = args or []
        self.kwargs = kwargs or {}
        self.finished = threading.Event()
        self.started_time: Optional[float] = None
        self.name = self.parent.name

        BenchmarkTimer._timers_count += 1
        BenchmarkTimer._timers[self.parent.name].append(self)

    @property
    def remaining_time(self) -> float:
        if self.started_time is None:
            raise RuntimeError("Timer hasn't been started yet")
        return self.interval - (perf_counter() - self.started_time)

    def start(self) -> None:
        BenchmarkTimer._started_timers_count += 1
        self.started_time = perf_counter()
        self.finished.clear()
        super().start()

    def cancel(self) -> None:
        self.finished.set()

    @classmethod
    def reset(cls) -> None:
        thread_name = threading.current_thread().name
        if timers := cls._timers.get(thread_name):
            for timer in timers[:]:  # Create copy for iteration
                timer.cancel()
            cls._timers[thread_name].clear()
            del cls._timers[thread_name]

    def run(self) -> None:
        try:
            if not self.finished.wait(self.interval):
                core.Kernel().defer(lambda: self.function(*self.args, **self.kwargs))
        except Exception as e:
            self.logger.error(f"Error in timer execution: {e}")
        finally:
            self.finished.set()
            self._cleanup()

    def _cleanup(self) -> None:
        thread_timers = BenchmarkTimer._timers[self.parent.name]
        if self in thread_timers:
            thread_timers.remove(self)

        if not thread_timers:
            del BenchmarkTimer._timers[self.parent.name]

        BenchmarkTimer._started_timers_count -= 1
        BenchmarkTimer._timers_count -= 1

    def __repr__(self) -> str:
        return (
            f"BenchmarkTimer(function={self.caller_name}, "
            f"interval={self.interval}, "
            f"active={'not finished' if not self.finished.is_set() else 'finished'})"
        )
