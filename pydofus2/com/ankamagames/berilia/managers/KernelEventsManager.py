import threading
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton
from whistle import Event, EventDispatcher
from enum import Enum
logger = Logger('KernelEventsManager')
class KernelEvts(Enum):
    MOVEMENT_STOPPED = 0
    SERVERS_LIST = 1
    CHARACTERS_LIST = 2
    CRASH = 3
    LOGGED_IN = 4
    IN_GAME = 5
    DEAD = 6
    ALIVE = 7
    ACTORSHOWED = 8
    CHARACTER_SELECTION_SUCCESS = 9
    SHUTDOWN = 10
    RESTART = 11
class KernelEventsManager(EventDispatcher, metaclass=Singleton):
    __waiting_evts: list[threading.Event]
    __crashMessage = None
    def __init__(self):
        super().__init__()
        self.__waiting_evts = list[threading.Event]()
        self.__crashMessage = None
        
    def wait(self, event: KernelEvts, timeout: float = None):
        received = threading.Event()
        ret = [None]
        def onReceived(e, *args, **kwargs):
            received.set()
            ret[0] = kwargs.get('return_value', None) 
        self.once(event, onReceived)
        self.__waiting_evts.append(received)
        received.wait(timeout)
        if received in self.__waiting_evts:
            self.__waiting_evts.remove(received)
        elif self.__crashMessage:
            raise Exception(self.__crashMessage)
        return ret[0]
    
    def on(self, event: KernelEvts, callback):
        self.add_listener(event, callback)
    
    def once(self, event: KernelEvts, callback):
        def onEvt(e, *args, **kwargs):
            self.remove_listener(e, onEvt)
            callback(e, *args, **kwargs)
        self.add_listener(event, onEvt)
    
    def send(self, event_id: KernelEvts, *args, **kwargs):
        if event_id == KernelEvts.CRASH:
            self.__crashMessage = kwargs.get('message', None)
        event = Event()
        event.sender = self
        event.name = event_id
        if event_id not in self._listeners:
            return event
        for listener in self.get_listeners(event_id):
            listener(event, *args, **kwargs)
            if event.propagation_stopped: break
    
    def reset(self):
        self.stopAllwaiting()
        self._listeners.clear()
        
    def stopAllwaiting(self):
        for evt in self.__waiting_evts:
            evt.set()
        self.__waiting_evts.clear()
