import errno
import functools
import math
import queue
import socket
import sys
import threading as mp
import traceback
from time import perf_counter
from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.network.MessageReceiver import \
    MessageReceiver
from pydofus2.com.ankamagames.dofus.network.messages.common.NetworkDataContainerMessage import \
    NetworkDataContainerMessage
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.ConnectedMessage import \
    ConnectedMessage
from pydofus2.com.ankamagames.jerakine.messages.ConnectionProcessCrashedMessage import \
    ConnectionProcessCrashedMessage
from pydofus2.com.ankamagames.jerakine.network.CustomDataWrapper import \
    ByteArray
from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.jerakine.network.INetworkMessage import \
        INetworkMessage

LOCK = mp.Lock()


def sendTrace(func):
    @functools.wraps(func)
    def wrapped(self: "ServerConnection", *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            _, exc_value, exc_traceback = sys.exc_info()
            traceback_in_var = traceback.format_tb(exc_traceback)
            error_trace = "\n".join(traceback_in_var) + "\n" + str(exc_value)
            cause = e.__cause__
            while cause:
                cause_traceback = traceback.format_tb(cause.__traceback__)
                error_trace += "\n\n-- Chained Exception --\n"
                error_trace += "\n".join(cause_traceback) + "\n" + str(cause)
                cause = cause.__cause__
            self._put(ConnectionProcessCrashedMessage(error_trace))

    return wrapped


class ServerConnection(mp.Thread):

    DEBUG_VERBOSE: bool = False
    LOG_ENCODED_CLIENT_MESSAGES: bool = False
    DEBUG_LOW_LEVEL_VERBOSE: bool = False
    DEBUG_DATA: bool = False
    LATENCY_AVG_BUFFER_SIZE: int = 200
    MESSAGE_SIZE_ASYNC_THRESHOLD: int = 300 * 1024
    CONNECTION_TIMEOUT = 7

    def __init__(self, id: str = "ServerConnection", receptionQueue: queue.Queue = None):
        super().__init__(name=mp.current_thread().name)
        self.id = id
        self._latencyBuffer = []
        self._remoteSrvHost = None
        self._remoteSrvPort = None

        self._connecting = mp.Event()
        self.connected = mp.Event()
        self._closing = mp.Event()
        self._paused = mp.Event()
        self.finished = mp.Event()

        self.stream = ByteArray()
        self.pauseQueue = list["INetworkMessage"]()
        self.sendingQueue = list["INetworkMessage"]()

        self._sendSequenceId: int = 0
        self._latestSent = 0
        self._lastSent = None
        self._lastSentPingTime = None

        self._firstConnectionTry: bool = True
        if receptionQueue is None:
            self.receptionQueue = queue.Queue(200)
        else:
            self.receptionQueue = receptionQueue

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connectionTimeout = None
        self.nbrSendFails = 0
        self._asyncNetworkDataContainerMessage: NetworkDataContainerMessage = None

    @property
    def latencyAvg(self) -> float:
        if len(self._latencyBuffer) == 0:
            return 0
        total = 0
        for latency in self._latencyBuffer:
            total += latency
        return round(1000 * total / len(self._latencyBuffer), 2)

    @property
    def latencyVar(self) -> float:
        avg = self.latencyAvg
        if len(self._latencyBuffer) == 0:
            return 0
        total = 0
        for latency in self._latencyBuffer:
            total += math.pow(latency - avg, 2)
        total = math.sqrt(total / len(self._latencyBuffer))
        return round(total, 2)

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
    def open(self) -> bool:
        return self.connected.is_set()

    @property
    def connecting(self) -> bool:
        return self._connecting.is_set()

    @property
    def paused(self) -> bool:
        return self._paused.is_set()

    def _put(self, msg):
        if not self._paused.is_set():
            self.receptionQueue.put(msg)
        else:
            self.pauseQueue.append(msg)

    @sendTrace
    def close(self) -> None:
        if self.closed or self.finished.is_set():
            Logger().warn(f"[{self.id}] Tried to close a socket while it had already been disconnected.")
            return
        Logger().debug(f"[{self.id}] Closing connection...")
        self.socket.close()
        self.sendingQueue.clear()
        self._closing.set()

    @sendTrace
    def send(self, msg: "NetworkMessage") -> None:
        if not self.open:
            if self.connecting:
                self.sendingQueue.append(msg)
                return Logger().warning(f"Message {msg} was queued")
            elif self._closing.is_set() or self.closed:
                return Logger().warning(f"Discarded Message {msg}")
        Logger().debug(f"[{self.id}] [SND] > {msg}")
        try:
            data = msg.pack()
            total_sent = 0
            if type(msg).__name__ == "BasicPingMessage":
                self._lastSentPingTime = perf_counter()
            while total_sent < len(data):
                sent = self.socket.send(data[total_sent:])
                if sent == 0:
                    raise RuntimeError("Socket connection broken")
                total_sent += sent
        except OSError as e:
            Logger().error(f"{e.errno}, {errno.errorcode[e.errno]} OS error received")
            if e.errno == errno.WSAECONNABORTED:
                self.nbrSendFails += 1
                if self.nbrSendFails > 3:
                    return self.close()
                self.send(msg)
        self.nbrSendFails = 0
        self._latestSent = perf_counter()
        self._lastSent = perf_counter()
        self._sendSequenceId += 1

    def pause(self) -> None:
        self._paused.set()

    @sendTrace
    def resume(self) -> None:
        self._paused.clear()
        while self.pauseQueue and not self.paused:
            msg = self.pauseQueue.pop(0)
            if self.DEBUG_DATA:
                Logger().debug(f"[{self.id}] [RCV] (after Resume) {msg}")
            self.receptionQueue.put(msg)

    @sendTrace
    def updateLatency(self) -> None:
        if self._paused.is_set() or len(self.pauseQueue) > 0 or self._latestSent == 0:
            return
        packetReceived = perf_counter()
        latency = packetReceived - self._latestSent
        self._latestSent = 0
        self._latencyBuffer.append(latency)
        if len(self._latencyBuffer) > self.LATENCY_AVG_BUFFER_SIZE:
            self._latencyBuffer.pop(0)

    @property
    def latencyMax(self) -> float:
        if len(self._latencyBuffer) == 0:
            return 0.3
        return max(self._latencyBuffer)

    def stopConnectionTimeout(self) -> None:
        if self.connectionTimeout:
            self.connectionTimeout.cancel()

    def onConnect(self) -> None:
        Logger().debug(f"[{self.id}] Connection established.")
        self.stopConnectionTimeout()
        self._connecting.clear()
        self.connected.set()
        for msg in self.sendingQueue:
            self.send(msg)
        self.stream = ByteArray()
        self.receptionQueue.put(ConnectedMessage())

    @sendTrace
    def receive(self) -> "INetworkMessage":
        return self.receptionQueue.get()

    def onClose(self, err) -> None:
        self.stopConnectionTimeout()
        Logger().debug(f"[{self.id}] Connection closed. {err}")
        self.connected.clear()
        from pydofus2.com.ankamagames.jerakine.network.ServerConnectionClosedMessage import \
            ServerConnectionClosedMessage

        self.receptionQueue.put(ServerConnectionClosedMessage(self.id))
        self.finished.set()
        Logger().info(f"[{self.id}] Finished.")
        if err:
            raise err

    @property
    def closed(self) -> bool:
        return self._closing.is_set()

    def onConnectionTimeout(self) -> None:
        from pydofus2.com.ankamagames.jerakine.network.messages.ServerConnectionFailedMessage import \
            ServerConnectionFailedMessage

        self.stopConnectionTimeout()
        if self.connected.is_set() or self.finished.is_set() or self._closing.is_set():
            return
        self._connecting.clear()
        if self._firstConnectionTry:
            Logger().debug(f"[{self.id}] Connection timeout, but WWJD ? Give a second chance !")
            self._firstConnectionTry = False
            self.connect(self._remoteSrvHost, self._remoteSrvPort)
        else:
            self.receptionQueue.put(ServerConnectionFailedMessage(self.id, "Connection timeout!"))

    @sendTrace
    def connect(self, host: str, port: int, timeout=CONNECTION_TIMEOUT) -> None:
        self.stream = ByteArray()
        if self.connecting:
            Logger().warn(f"[{self.id}] Tried to connect while already connecting.")
            return
        self.connected.clear()
        self._connecting.set()
        self._closing.clear()
        self._firstConnectionTry = True
        self._remoteSrvHost = host
        self._remoteSrvPort = port
        Logger().info(f"[{self.id}] Connecting to {host}:{port}...")
        self.socket.connect((host, port))

    def handleMessage(self, msg: NetworkMessage, from_client=False):
        if self.closed or not self.connected:
            return
        if msg is None:
            return
        if type(msg).__name__ == "BasicPongMessage" and self._lastSentPingTime:
            latency = round(1000 * (perf_counter() - self._lastSentPingTime), 2)
            Logger().info(f"Latency : {latency}ms, average {self.latencyAvg}, var {self.latencyVar}")
        if msg.unpacked:
            msg.receptionTime = perf_counter()
            msg.sourceConnection = self.id
            if type(msg).__name__ == "NetworkDataContainerMessage":
                Logger().debug(f"Received network Datacontainer with content of size : {len(msg.content)}")
                MessageReceiver().parse(ByteArray(msg.content), self.handleMessage, from_dataContainer=True)
            else:
                self._put(msg)

    @sendTrace
    def run(self):
        err = ""
        while not self._closing.is_set() and not self.finished.is_set():
            try:
                rdata = self.socket.recv(8900)
                if rdata:
                    if self._connecting.is_set():
                        Logger().debug(f"Received {len(rdata)}bytes from server!")
                        self.onConnect()
                    self.stream += rdata
                    MessageReceiver().parse(self.stream, self.handleMessage)
                else:
                    Logger().debug(f"[{self.id}] Connection closed by remote host")
                    self._closing.set()
            except (KeyboardInterrupt, SystemExit) as e:
                Logger().debug(f"[{self.id}] Interrupted suddenly!")
                self._closing.set()
                err = e
            except OSError as e:
                if e.errno == errno.WSAENOTCONN:
                    Logger().debug(f"[{self.id}] Waiting for socket to connect...")
                    self._closing.wait(0.5)
                elif e.errno == errno.WSAECONNABORTED:
                    Logger().debug(f"[{self.id}] Connection aborted by user.")
                    self._closing.set()
                elif e.errno == errno.WSAECONNRESET:
                    Logger().debug(f"[{self.id}] Connection reset by peer.")
                    self._closing.set()
                elif e.errno == errno.WSAENOTSOCK:
                    Logger().debug(f"[{self.id}] Socket apears to be closed.")
                    if not self._closing.is_set():
                        err = e
                        self._closing.set()
                elif e.errno == errno.WSAETIMEDOUT:
                    Logger().debug(f"[{self.id}] Connection timed out.")
                    if self._connecting.is_set():
                        self.onConnectionTimeout()
                else:
                    Logger().debug(f"{e.errno}, {errno.errorcode[e.errno]} OS error received")
                    err = e
                    self._closing.set()
        self.onClose(err)
