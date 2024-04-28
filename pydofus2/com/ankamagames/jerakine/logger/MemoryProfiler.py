import functools
import os
import sys
import threading
import traceback
import tracemalloc

# import objgraph
import psutil

from pydofus2.com.ankamagames.jerakine.metaclass.ThreadSharedSingleton import ThreadSharedSingleton


class MemoryProfiler(threading.Thread, metaclass=ThreadSharedSingleton):
    SHOW_LIMIT = 100
    KEY_TYPE = "lineno"
    _process = psutil.Process(os.getpid())
    _memory_usage = {}

    def __init__(self, threshold=1024 * 1024 * 3, file_name="memory_usage_h.txt"):
        super().__init__(name="MemoryProfiler")
        self.threshold = threshold
        self.file_name = file_name
        self.stop_event = threading.Event()

    @classmethod
    def track_memory(cls, name):
        def actual_wrapper(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                memory_before = cls._process.memory_info().rss
                result = func(*args, **kwargs)
                memory_after = cls._process.memory_info().rss
                memory_delta = memory_after - memory_before
                cls._memory_usage[name] = {
                    "usage": cls._memory_usage.get(name, {}).get("usage", 0) + memory_delta,
                    "count": cls._memory_usage.get(name, {}).get("count", 0) + 1,
                }
                return result

            return wrapper

        return actual_wrapper

    def run(self):
        try:
            format_row = "{:<40} {:>20} {:>20}\n"
            row_delimiter = "-" * 83 + "\n"
            headears = format_row.format("function", "usage", "count")
            while not self.stop_event.is_set():
                with open(self.file_name, "w") as fp:
                    fp.write("Tracked Functions memory usage:\n")
                    fp.write(headears)
                    fp.write(row_delimiter)
                    for key, value in self._memory_usage.items():
                        fmt_usage = tracemalloc._format_size(value["usage"], False)
                        fp.write(format_row.format(key, fmt_usage, value["count"]))
                    fp.write(row_delimiter)
                    total = tracemalloc._format_size(self._process.memory_info().rss, False)
                    fp.write(f"Total memory usage: {total}\n")
                    fp.write(row_delimiter)
                    objgraph.show_growth(file=fp)
                self.stop_event.wait(10)
        except Exception as e:
            with open(self.file_name, "a") as fp:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback_in_var = traceback.format_tb(exc_traceback)
                error_trace = (
                    str(e) + "\n" + str(exc_type) + "\n" + str(exc_value) + "\n" + "\n".join(traceback_in_var)
                )
                fp.write(error_trace)

    def stop(self):
        self.stop_event.set()
