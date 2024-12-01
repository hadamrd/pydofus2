import threading
from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.berilia.managers.EventsHandler import EventsHandler


class Listener:
    def __init__(
        self,
        manager: "EventsHandler",
        event_id,
        callback: callable,
        timeout=None,
        ontimeout=None,
        once=False,
        priority=0,
        originator=None,
    ):
        self._deleted = False
        self.event_id = event_id
        self.callback = callback
        self.timeout = timeout
        self.timeoutCallback = ontimeout
        self.timeoutTimer = None
        if timeout:
            self.armTimer()
        self.once = once
        self.priority = priority
        self.manager = manager
        self.thname = threading.current_thread().name
        self.originator = originator
        self.nbrTimeouts = 0

    def call(self, event, *args, **kwargs):
        if self._deleted:
            # Logger().warning("Callback called of a deleted listener")
            return
        self.cancelTimer()
        self.callback(event, *args, **kwargs)

    def delete(self):
        self._deleted = True
        self.cancelTimer()
        if self.event_id not in self.manager._listeners:
            return Logger().warning("Trying to delete Event not registered")
        listeners = self.manager._listeners[self.event_id][self.priority]
        if self in listeners:
            listeners.remove(self)
            if self.event_id in self.manager._sorted:
                del self.manager._sorted[self.event_id]

    def armTimer(self, newTimeout=None):
        if self._deleted:
            return Logger().warning("arm timer of a deleted listener")
        if newTimeout:
            self.timeout = newTimeout
        from pydofus2.com.ankamagames.jerakine.benchmark.BenchmarkTimer import BenchmarkTimer

        self.timeoutTimer = BenchmarkTimer(self.timeout, lambda: self.timeoutCallback(self))
        self.timeoutTimer.start()

    def cancelTimer(self):
        if self.timeoutTimer:
            self.timeoutTimer.cancel()

    def __str__(self):
        summary = f"Listener(event_id={self.event_id}, priority={self.priority}, callback={self.callback.__name__}, "
        if self.timeoutTimer and not self.timeoutTimer.finished.is_set():
            remaining_time = self.timeoutTimer.remaining_time()
            summary += f"timeout={self.timeout}, time_left={remaining_time})"
        else:
            summary += f"timeout={self.timeout})"
        return summary
