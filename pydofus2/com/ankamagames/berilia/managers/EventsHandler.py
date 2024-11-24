import operator
import threading
from collections import defaultdict
from typing import Any, Callable, DefaultDict, Dict, List, Optional

from pydofus2.com.ankamagames.berilia.managers.Listener import Listener
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger

lock = threading.RLock()


class Event:
    def __init__(self):
        self.propagation_stopped: bool = False
        self.sender: "EventsHandler"
        self.name: Any
        self.listener: "Listener"

    def stop_propagation(self) -> None:
        self.propagation_stopped = True


class EventsHandler:
    def __init__(self, name: str = "Unknown"):
        super().__init__()
        # Default dict for listeners: event_id -> priority -> listeners
        self._listeners: DefaultDict[str, DefaultDict[int, List[Listener]]] = defaultdict(lambda: defaultdict(list))
        self._sorted: Dict[str, List[Listener]] = {}
        self.__waiting_events: List[threading.Event] = []
        self._crash_message: Optional[str] = None
        self.name = name
        self.origin_thread = threading.current_thread().name
        self.logger = Logger()

    def has_listener(self, event_id: str) -> bool:
        return bool(self._listeners[event_id])

    def wait(self, event: str, timeout: Optional[float] = None, originator: Any = None) -> tuple:
        received = threading.Event()
        ret = [None]

        def on_received(e: Event, *args, **kwargs) -> None:
            received.set()
            ret[0] = (*args, *kwargs)

        self.once(event, on_received, originator=originator)
        self.__waiting_events.append(received)

        wait_result = received.wait(timeout)
        if received in self.__waiting_events:
            self.__waiting_events.remove(received)

        if self._crash_message:
            raise Exception(self._crash_message)
        if not wait_result:
            raise TimeoutError(f"wait event {event} timed out")

        return ret[0]

    def on(
        self,
        event_id: str,
        callback: Callable,
        priority: int = 0,
        timeout: Optional[float] = None,
        ontimeout: Optional[Callable] = None,
        once: bool = False,
        originator: Any = None,
        retry_count: Optional[int] = None,
        retry_action: Optional[Callable] = None,
    ) -> Optional[Listener]:
        def on_listener_timeout(listener: Listener) -> None:
            if retry_count:
                listener.nbrTimeouts += 1
                if listener.nbrTimeouts > retry_count:
                    return ontimeout(listener)
                listener.armTimer()
                if retry_action:
                    retry_action()
            else:
                ontimeout(listener)

        listener = Listener(self, event_id, callback, timeout, on_listener_timeout, once, priority, originator)

        self._listeners[event_id][priority].append(listener)
        self._sorted.pop(event_id, None)  # Clear sorted cache if exists
        return listener

    def on_multiple(self, listeners: List[tuple[str, Callable]], originator: Any = None) -> None:
        for event_id, callback in listeners:
            self.on(event_id, callback, originator=originator)

    def once(
        self,
        event_id: str,
        callback: Callable,
        priority: int = 0,
        timeout: Optional[float] = None,
        ontimeout: Optional[Callable] = None,
        originator: Any = None,
        retry_nbr: Optional[int] = None,
        retry_action: Optional[Callable] = None,
    ) -> Optional[Listener]:
        return self.on(
            event_id,
            callback,
            priority,
            timeout,
            ontimeout,
            once=True,
            originator=originator,
            retry_count=retry_nbr,
            retry_action=retry_action,
        )

    def sort_listeners(self, event_id: str) -> None:
        # Flatten and sort listeners by priority
        self._sorted[event_id] = [
            listener
            for priority, listeners in sorted(self._listeners[event_id].items(), key=operator.itemgetter(0))
            for listener in listeners
        ]

    def get_sorted_listeners(self, event_id: Optional[str] = None) -> List[Listener]:
        if event_id is not None:
            if event_id not in self._sorted:
                self.sort_listeners(event_id)
            return self._sorted[event_id]

        # Sort all events if no specific event_id provided
        for evt_id in self._listeners:
            if evt_id not in self._sorted:
                self.sort_listeners(evt_id)
        return []

    def send(self, event_id: str, *args, **kwargs) -> Event:
        event = Event()
        event.sender = self
        event.name = event_id

        if not self._listeners[event_id]:
            return event

        event_listeners = self.get_sorted_listeners(event_id)
        to_remove: List[Listener] = []

        for listener in event_listeners:
            event = Event()
            event.sender = self
            event.name = event_id
            event.listener = listener

            if self.origin_thread == threading.current_thread().name:
                listener.call(event, *args, **kwargs)
            else:
                from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel

                Kernel.getInstance(self.origin_thread).defer(lambda: listener.call(event, *args, **kwargs))

            if listener.once:
                to_remove.append(listener)

            if event.propagation_stopped:
                break

        if to_remove:
            with lock:
                self._sorted.pop(event_id, None)
                for listener in to_remove:
                    listener.delete()

        return event

    def reset(self) -> None:
        self.stop_all_waiting()
        for listener in self.iter_listeners():
            listener.delete()
        self._listeners.clear()
        self._sorted.clear()
        self.logger.debug(f"Events manager {self.name} reset")

    def iter_listeners(self) -> List[Listener]:
        return [
            listener
            for priorities in self._listeners.values()
            for listeners in priorities.values()
            for listener in listeners
        ]

    def stop_all_waiting(self) -> None:
        for evt in self.__waiting_events:
            evt.set()
        self.__waiting_events.clear()

    def remove_listeners(self, event_id: str, callbacks: List[Callable]) -> None:
        if not self._listeners[event_id]:
            return self.logger.warning(f"Event {event_id} not found")

        for priority, listeners in self._listeners[event_id].items():
            self._listeners[event_id][priority] = [l for l in listeners if l.callback not in callbacks]
        self._sorted.pop(event_id, None)

    def remove_listener(self, event_id: str, callback: Callable) -> None:
        if not self._listeners[event_id]:
            return self.logger.warning(f"Event {event_id} not found")

        for priority, listeners in self._listeners[event_id].items():
            self._listeners[event_id][priority] = [l for l in listeners if l.callback != callback]
        self._sorted.pop(event_id, None)

    def get_listeners_by_origin(self, origin: Any) -> List[Listener]:
        return [
            listener
            for priorities in self._listeners.values()
            for listeners in priorities.values()
            for listener in listeners
            if not listener._deleted and listener.originator and listener.originator == origin
        ]

    def clear_all_by_origin(self, origin: Any) -> None:
        for listener in self.get_listeners_by_origin(origin):
            listener.delete()
