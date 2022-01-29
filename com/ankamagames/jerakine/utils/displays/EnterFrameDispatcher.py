import logging
from threading import Event
from time import perf_counter
from types import FunctionType
from com.ankamagames.jerakine.managers import Worker
from com.ankamagames.jerakine.metaclasses.singleton import Singleton
logger = logging.getLogger("bot")



class EnterFrameDispatcher(metaclass=Singleton):
    
    def __init__(self):
        self._maxAllowedTime:int = 20
        self._listenerUp:bool = False
        self._workerListenerUp:bool = False
        self._currentTime:int = None
        self._postWorkerTime:int = None
        self._diff:int = 0 
        self._noWorkerFrameCount:int = 0
        self._controledListeners:dict = dict(True)
        self._worker:Worker = None
    
    
    def addWorker(self, w:Worker) -> None:
        self._worker = w
        if not self._listenerUp:
            self._listenerUp = True
        if not self._workerListenerUp:
            self._workerListenerUp = True
    
    def removeWorker(self) -> None:
        if self._workerListenerUp:
            self._workerListenerUp = False
        
    @property
    def enterFrameListenerCount(self) -> int:
        key = None
        count:int = 0
        for key in self._controledListeners:
            count += 1
        return count
    
    @property
    def controledEnterFrameListeners(self) -> dict:
        return self._controledListeners
    
    @property
    def worker(self) -> Worker:
        return self._worker
        
    def addEventListener(self, listener:FunctionType, name:str, frameRate:int = 4.294967295E9) -> None:
        if not self._controledListeners[listener]:
            exp1 = 0 if frameRate == float("inf") else int(1000 / frameRate)
            self._controledListeners[listener] = ControledEnterFrameListener(name, listener, frameRate <= 0 or exp1, int(self._currentTime) if not self._listenerUp else int(perf_counter()))
            if not self._listenerUp:
                self._listenerUp = True
    
    def hasEventListener(self, listener:FunctionType) -> bool:
        return self._controledListeners[listener] != None
    
    @property
    def maxAllowedTime(self) -> int:
        return self._maxAllowedTime

    @maxAllowedTime.setter
    def maxAllowedTime(self, time:int) -> None:
        self._maxAllowedTime = time
    
    def removeEventListener(self, listener:FunctionType) -> None:
        if self._controledListeners[listener]:
            del self._controledListeners[listener]
            if len(self._controledListeners) == 0 and not self._workerListenerUp:
                self._listenerUp = False
    
    def handleEnterFrameEvents(self, e:Event) -> None:
        cefl:ControledEnterFrameListener = None
        self._currentTime = perf_counter()
        for cefl in self._controledListeners:
            diff = self._currentTime - cefl.latestChange
            if diff > cefl.wantedGap - cefl.overhead:
                cefl.listener(e)
                cefl.latestChange = self._currentTime
                cefl.overhead = diff - cefl.wantedGap + cefl.overhead
    
    def remainsTime(self) -> bool:
        return perf_counter() - self._postWorkerTime < self._maxAllowedTime
    
    def handleWorkers(self, e:Event) -> None:
        _diff = perf_counter() - self._postWorkerTime
        if _diff < self._maxAllowedTime:
            self._worker.processQueues(self._maxAllowedTime - _diff)
            self._noWorkerFrameCount = 0
        else:
            self._worker.processQueues(self._noWorkerFrameCount)
            if self._noWorkerFrameCount < self._maxAllowedTime / 2:
                self._noWorkerFrameCount += 1
        self._postWorkerTime = perf_counter()


class ControledEnterFrameListener:

    name:str
    listener:FunctionType
    wantedGap:int
    overhead:int
    latestChange:int

    def __init__(self, name:str, listener:FunctionType, wantedGap:int, latestChange:int):
        super().__init__()
        self.name = name
        self.listener = listener
        self.wantedGap = wantedGap
        self.latestChange = latestChange
