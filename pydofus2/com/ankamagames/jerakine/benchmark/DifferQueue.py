import logging
from collections import defaultdict
from queue import Queue
from threading import Event, Lock, Thread, current_thread
from typing import Dict, Tuple

# Setup basic logging
logging.basicConfig(level=logging.INFO)
Logger = logging.getLogger()


class DeferQueue:
    _queues: Dict[str, Tuple[Queue, Thread, Event]] = {}
    _lock = Lock()
    _shutdown = defaultdict(Event)

    @classmethod
    def get_queue(cls, thread_name: str) -> Queue:
        with cls._lock:
            if thread_name not in cls._queues:
                q = Queue()
                stop_event = Event()

                def worker():
                    while not stop_event.is_set():
                        try:
                            func, args, kwargs = q.get()
                            if func is None:  # Sentinel
                                logging.info("sentinel received")
                                q.task_done()
                                break
                            try:
                                func(*args, **kwargs)
                            finally:
                                q.task_done()
                        except Exception as e:
                            logging.error(f"Error in worker: {e}")
                    logging.info(f"Worker for {thread_name} stopped")

                t = Thread(target=worker, daemon=True)
                t.name = thread_name
                t.start()
                cls._queues[thread_name] = (q, t, stop_event)
            return cls._queues[thread_name][0]

    @classmethod
    def defer(cls, func, *args, **kwargs):
        thread_name = current_thread().name
        if cls._shutdown[thread_name].is_set():
            logging.warning("Deferring during shutdown - executing immediately")
            func(*args, **kwargs)
            return

        q = cls.get_queue(thread_name)
        q.put((func, args, kwargs))

    @classmethod
    def cleanup_thread(cls, thread_name: str) -> None:
        if thread_name in cls._queues:
            q, t, stop_event = cls._queues[thread_name]
            q.put((None, [], {}))
            q.join()
            stop_event.set()
            t.join()

    @classmethod
    def shutdown(cls) -> None:
        thread_name = current_thread().name
        if cls._shutdown[thread_name].is_set():
            return

        cls._shutdown[thread_name].set()
        logging.info("Starting DeferQueue shutdown...")
        with cls._lock:
            logging.info("Lock acquired to shutdown")
            for thread_name in list(cls._queues.keys()):
                cls.cleanup_thread(thread_name)
            del cls._shutdown[thread_name]
        logging.info("DeferQueue shutdown complete")
