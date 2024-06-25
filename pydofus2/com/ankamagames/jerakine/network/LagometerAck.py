import threading
from time import perf_counter

from pydofus2.com.ankamagames.dofus.network.messages.game.basic.BasicAckMessage import BasicAckMessage
from pydofus2.com.ankamagames.jerakine.benchmark.BenchmarkTimer import BenchmarkTimer
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.network.INetworkMessage import INetworkMessage
from pydofus2.com.ankamagames.jerakine.network.Lagometer import Lagometer


class LagometerAck(Lagometer):

    _msgTimeStack: list[int]

    _active: threading.Event

    _optionId: int

    def __init__(self):
        self._timer = None
        self._msgTimeStack = list[int]()
        super().__init__()

    def stop(self) -> None:
        if self._timer:
            self._timer.cancel()
        self._msgTimeStack = []

    def ping(self, msg: INetworkMessage = None) -> None:
        if not self._msgTimeStack:
            if self._timer:
                self._timer.cancel()
            self._timer = BenchmarkTimer(self.SHOW_LAG_DELAY, self.onTimerComplete)
            self._timer.start()
        self._msgTimeStack.append(perf_counter())

    def pong(self, msg: INetworkMessage = None) -> None:
        if isinstance(msg, BasicAckMessage):
            latency = perf_counter() - self._msgTimeStack.pop(0)
            if latency > self.SHOW_LAG_DELAY:
                Logger().debug(f"[Lagometer] {latency}ms de latence (based on ACK)")
                self.startLag()
                self._timer.cancel()
            else:
                self.stopLag()
                if self._msgTimeStack:
                    if self._timer:
                        self._timer.cancel()
                    self._timer = BenchmarkTimer(
                        max(
                            0,
                            self.SHOW_LAG_DELAY - (perf_counter() - self._msgTimeStack[0]),
                        ),
                        self.onTimerComplete,
                    )
                    self._timer.start()
                else:
                    self._timer.cancel()
