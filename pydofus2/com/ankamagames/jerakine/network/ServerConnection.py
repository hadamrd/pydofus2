import functools
from threading import Timer
from pathos.helpers import mp
import socket
from pydofus2.com.ankamagames.jerakine.benchmark.BenchmarkTimer import BenchmarkTimer
from time import perf_counter
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.ConnectedMessage import ConnectedMessage
from pydofus2.com.ankamagames.jerakine.messages.ConnectionProcessCrashedMessage import ConnectionProcessCrashedMessage
from pydofus2.com.ankamagames.jerakine.network.CustomDataWrapper import ByteArray
from pydofus2.com.ankamagames.jerakine.network.LagometerAck import LagometerAck
from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage
from pydofus2.com.ankamagames.dofus.network.MessageReceiver import MessageReceiver
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pydofus2.com.ankamagames.jerakine.network.INetworkMessage import INetworkMessage


logger = Logger()


class UnknowMessageId(Exception):
    pass

def sendTrace(func):
    @functools.wraps(func)
    def wrapped(self: 'ServerConnection', *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except:
            logger.error(f"[{self.id}] Error while reading socket. \n", exc_info=True)
            import sys
            import traceback
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback_in_var = traceback.format_tb(exc_traceback)
            error_trace = str(exc_type) + "\n" + str(exc_value) + "\n" + "\n".join(traceback_in_var)
            self.close()
            self._receptionQueue.put(ConnectionProcessCrashedMessage(error_trace))

    return wrapped
class ServerConnection(mp.Process):

    DEBUG_VERBOSE: bool = False
    LOG_ENCODED_CLIENT_MESSAGES: bool = False
    DEBUG_LOW_LEVEL_VERBOSE: bool = False
    DEBUG_DATA: bool = True
    LATENCY_AVG_BUFFER_SIZE: int = 50
    MESSAGE_SIZE_ASYNC_THRESHOLD: int = 300 * 1024
    CONNECTION_TIMEOUT = 7

    def __init__(self, host: str = None, port: int = 0, id: str = ""):
        self._latencyBuffer = []
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._remoteSrvHost = host
        self._remoteSrvPort = port
        self.id = id

        self._connectingToServer = mp.Event()
        self._ServerConnected = mp.Event()
        self._closedConnection = mp.Event()
        self._paused = mp.Event()
                
        self._packetId = None
        self._msgLenLength = None
        self._messageLength = None
        
        self.__receivedStream = ByteArray()
        self.__pauseQueue = list['INetworkMessage']()
        self._sendingQueue = list['INetworkMessage']()
    
        self._sendSequenceId: int = 0
        self._latestSent: int = 0
        self._lastSent: int = None

        self._firstConnectionTry: bool = True
        self._connectionTimeout = None
        self._lagometer = LagometerAck()
        self._rawParser = MessageReceiver()

        self._receptionQueue = mp.Queue(200)
        super().__init__(name=self.id)

    @property
    def latencyAvg(self) -> int:
        if len(self._latencyBuffer) == 0:
            return 0
        total: int = 0
        for latency in self._latencyBuffer:
            total += latency
        return int(total / len(self._latencyBuffer))

    @property
    def latencySamplesCount(self) -> int:
        return len(self._latencyBuffer)
    
    @property
    def latencySamplesMax(self) -> int:
        return self.LATENCY_AVG_BUFFER_SIZE
    
    @property
    def port(self) -> int:
        return self._remoteSrvPort

    @property
    def host(self) -> int:
        return self._remoteSrvHost

    @property
    def lastSent(self) -> int:
        return self._lastSent

    @property
    def sendSequenceId(self) -> int:
        return self._sendSequenceId

    @property
    def connected(self) -> bool:
        return self._ServerConnected.is_set()

    @property
    def connecting(self) -> bool:
        return self._connectingToServer.is_set()
    
    @property
    def paused(self) -> bool:
        return self._paused.is_set()

    @sendTrace
    def connect(self, host: str, port: int) -> None:
        if self.connecting:
            logger.warn(f"[{self.id}] Tried to connect while already connecting.")
            return
        self._connectionTimeout = BenchmarkTimer(self.CONNECTION_TIMEOUT, self.onConnectionTimeout)
        self._connectionTimeout.start()
        self.start()
        self._ServerConnected.clear()
        self._connectingToServer.set()
        self._closedConnection.clear()
        self._firstConnectionTry = True
        self._remoteSrvHost = host
        self._remoteSrvPort = port
        logger.info(f"[{self.id}] Connecting to {host}:{port}...")
        self._socket.connect((host, port))

    @sendTrace
    def close(self) -> None:
        if self._connectionTimeout:
            self._connectionTimeout.cancel()
        if self.closed:
            logger.warn(f"[{self.id}] Tried to close a socket while it had already been disconnected.")
            return
        logger.debug(f"[{self.id}] Closing connection!")
        self._closedConnection.set()
        self._socket.close()  
    
    @sendTrace
    def send(self, msg: 'INetworkMessage') -> None:
        if not self.connected:
            if self.connecting:
                self._sendingQueue.append(msg)
            return
        if self.DEBUG_DATA:
            logger.debug(f"[{self.id}] [SND] > {msg}")
        self._socket.send(msg.pack())
        self._latestSent = perf_counter()
        self._lastSent = perf_counter()
        self._sendSequenceId += 1
        if self._lagometer:
            self._lagometer.ping(msg)


    def __str__(self) -> str:
        status = "Server connection status:\n"
        status += "  Connected:       " + ("Yes" if self._socket.connected else "No") + "\n"
        if self.connected:
            status += "  Connected to:    " + self._remoteSrvHost + ":" + self._remoteSrvPort + "\n"
        else:
            status += "  Connecting:      " + ("Yes" if self._connectingToServer else "No") + "\n"
        if self._connectingToServer:
            status += "  Connecting to:   " + self._remoteSrvHost + ":" + self._remoteSrvPort + "\n"
        status += "  Raw parser:      " + self.rawParser + "\n"
        if self._sendingQueue:
            status += "  Output buffer:   " + len(self._sendingQueue) + " message(s)\n"
        if self.__receivedStream:
            status += "  Input buffer:    " + len(self.__receivedStream) + " byte(s)\n"
        if self._handlingSplitedPckt:
            status += "  Splitted message in the input buffer:\n"
            status += "    Message ID:      " + self._packetId + "\n"
            status += "    Awaited length:  " + self._packetLength + "\n"
        return status

    def pause(self) -> None:
        self._paused.set()

    @sendTrace
    def resume(self) -> None:
        self._paused.clear()
        while self.__pauseQueue and not self.paused:
            msg = self.__pauseQueue.pop(0)
            if self.DEBUG_DATA:
                logger.debug(f"[self.id] [RCV] (after Resume) {msg}")
            self._receptionQueue.put(msg)

    @sendTrace
    def parseMessages(self, input: ByteArray) -> None:
        msg: NetworkMessage = self._parse(input)
        while msg is not None and not self.closed:
            input.trim()
            if self._lagometer:
                self._lagometer.pong(msg)
            msg.receptionTime = perf_counter()
            msg.sourceConnection = self.id
            self.process(msg)
            msg = self._parse(input)

    @sendTrace
    def process(self, msg: 'INetworkMessage') -> None:
        if msg.unpacked:
            if not self._paused.is_set():
                if self.DEBUG_DATA:
                    logger.debug(f"[{self.id}] [RCV] {msg}")
                self._receptionQueue.put(msg)
            else:
                self.__pauseQueue.append(msg)
                
    def _parse(self, buffer: ByteArray) -> NetworkMessage:
        if self._msgLenLength is None:     
            if buffer.remaining() < 2: return
            staticHeader = buffer.readUnsignedShort()
            self._packetId = staticHeader >> NetworkMessage.BIT_RIGHT_SHIFT_LEN_PACKET_ID
            if self._packetId not in self._rawParser._messagesTypes:
                raise UnknowMessageId(f"Unknown message id {self._packetId}")
            self._msgLenLength = staticHeader & NetworkMessage.BIT_MASK

        if self._messageLength is None:
            if buffer.remaining() < self._msgLenLength: return
            self._messageLength = int.from_bytes(buffer.read(self._msgLenLength), "big")
            
        if buffer.remaining() >= self._messageLength:
            self.updateLatency()
            msg = self._rawParser.parse(buffer, self._packetId, self._messageLength)
            self._packetId = None
            self._msgLenLength = None
            self._messageLength = None
            return msg

    @sendTrace
    def updateLatency(self) -> None:
        if self._paused.is_set() or len(self.__pauseQueue) > 0 or self._latestSent == 0:
            return
        packetReceived: int = perf_counter()
        latency: int = packetReceived - self._latestSent
        self._latestSent = 0
        self._latencyBuffer.append(latency)
        if len(self._latencyBuffer) > self.LATENCY_AVG_BUFFER_SIZE:
            self._latencyBuffer.pop(0)

    @sendTrace
    def onConnect(self) -> None:
        logger.debug(f"[{self.id}] Connection established with the socket.")
        if self._connectionTimeout is not None:
            self._connectionTimeout.cancel()      
        self._connectingToServer.clear()
        self._ServerConnected.set()
        for msg in self._sendingQueue:
            self.send(msg)
        self.__receivedStream = ByteArray()
        self._receptionQueue.put(ConnectedMessage())

    @sendTrace
    def receive(self) -> 'INetworkMessage':
        try:
            return self._receptionQueue.get()
        except KeyboardInterrupt:
            return None
    
    @sendTrace
    def onClose(self, err="") -> None:
        from pydofus2.com.ankamagames.jerakine.network.ServerConnectionClosedMessage import ServerConnectionClosedMessage
        if self._connectionTimeout is not None:
            self._connectionTimeout.cancel()       
        logger.debug(f"[{self.id}] Connection closed. {err}")
        if self._lagometer:
            self._lagometer.stop()
        try:
            self._socket.close()
        except: pass
        self._ServerConnected.clear()
        self._connectingToServer.clear()
        self._receptionQueue.put(ServerConnectionClosedMessage(self.id))

    @sendTrace
    def onConnectionTimeout(self) -> None:
        from pydofus2.com.ankamagames.jerakine.network.messages.ServerConnectionFailedMessage import ServerConnectionFailedMessage
        if self.connected:
            logger.warning(f"[{self.id}] Connection timeout, but we are connected ?")
            self._connectionTimeout.finished.set()
            return
        if self._lagometer:
            self._lagometer.stop()
        self._connectingToServer.clear()
        if self.closed:
            return
        if self._firstConnectionTry:
            logger.debug(f"[{self.id}] Connection timeout, but WWJD ? Give a second chance !")
            self.connect(self._remoteSrvHost, self._remoteSrvPort)
            self._firstConnectionTry = False
        else:
            self._receptionQueue.put(ServerConnectionFailedMessage(self.id, "Connection timeout!"))

    @property
    def closed(self) -> bool:
        return self._closedConnection.is_set()
    
    @sendTrace
    def run(self):
        err = ""
        if not self._connectingToServer.wait(20):
            raise Exception("Connection process started but no connection event received!")
        logger.info(f"[{self.id}] Will Start listening for incomming data from {self.host}:{self.port}")

        while not self.closed:
            try:
                rdata = self._socket.recv(2056)
                if rdata:
                    if self.connecting:
                        self.onConnect()
                    self.__receivedStream += rdata
                    self.parseMessages(self.__receivedStream)
                else:
                    break
            except OSError as e:
                logger.warning(f"[{self.id}] Error while reading data from socket: {e}")
                err = str(e)
        self.onClose(err)
        logger.info(f"[{self.id}] Stopped listening for incomming data")
