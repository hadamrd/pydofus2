import os

from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger

from .Packet import TCPPacket

LOW_LEVEL_DEBUG = os.environ.get("LOW_LEVEL_DEBUG", False)

class SnifferBuffer:
    
    def __init__(self, id="Sniffer Buffer"):
        self.id = id
        self.memory = list[TCPPacket]()
        self.buffer = None

    def insort_right(self, a: list[TCPPacket], x: TCPPacket, lo=0, hi=None):
        if len(a) == 0:
            return a.append(x)
        lo = self.bisect_right(a, x, lo, hi)
        if lo > 0 and a[lo-1].nxtseq == x.seq:
            a[lo-1].rappend(x)
            if lo < len(a) and a[lo-1].nxtseq == a[lo].seq:
                a[lo-1].rappend(a[lo])
                del a[lo]
        elif lo < len(a) and a[lo].seq == x.nxtseq:
            a[lo].lappend(x)
        else:
            a.insert(lo, x)
            
    def bisect_right(self, a, x, lo=0, hi=None):
        if lo < 0:
            raise ValueError('lo must be non-negative')
        if hi is None:
            hi = len(a)
        while lo < hi:
            mid = (lo+hi)//2
            if x < a[mid]: hi = mid
            else: lo = mid+1
        return lo

    def write(self, packet: TCPPacket):
        if LOW_LEVEL_DEBUG:
            Logger().debug(f"-----------------------------------------------------------------")
            Logger().debug(f"[{self.id}] buffer: {self.buffer}")
            Logger().debug(f"[{self.id}] memory: {self.memory}")
            Logger().debug(f"[{self.id}] write({packet})")
        if self.buffer is None:
            self.buffer = packet
            return True
        if packet.seq == self.buffer.nxtseq:
            self.buffer.rappend(packet)
            if len(self.memory) > 0 and self.memory[0].seq == self.buffer.nxtseq:
                self.buffer.rappend(self.memory.pop(0))
            return True
        elif packet.seq < self.buffer.nxtseq:
            if LOW_LEVEL_DEBUG:
                Logger().warning(f"[{self.id}] Received duplicate of {packet}, will discard it.")
        else:
            self.insort_right(self.memory, packet)
            Logger().warning(f"[{self.id}] Received {packet} out of order, memorysize = {len(self.memory)}.")
        return False
    
    def read(self) -> bytes:
        return self.buffer.data

    def trim(self):
        self.buffer.data.trim()
        
    def clear(self):
        self.buffer = None
        self.memory = list[TCPPacket]()
        
    def __repr__(self) -> str:
        return f"[data: {self.buffer.data} | memory: {self.memory}]"