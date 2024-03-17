import random
import threading
from time import perf_counter

from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionType import \
    ConnectionType
from pydofus2.com.ankamagames.dofus.kernel.net.DisconnectionReason import \
    DisconnectionReason
from pydofus2.com.ankamagames.dofus.kernel.net.DisconnectionReasonEnum import \
    DisconnectionReasonEnum
from pydofus2.com.ankamagames.dofus.kernel.net.PlayerDisconnectedMessage import \
    PlayerDisconnectedMessage
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import \
    PlayerManager
from pydofus2.com.ankamagames.dofus.network.messages.game.actions.GameActionAcknowledgementMessage import \
    GameActionAcknowledgementMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightTurnFinishMessage import \
    GameFightTurnFinishMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightTurnReadyMessage import \
    GameFightTurnReadyMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameMapMovementConfirmMessage import \
    GameMapMovementConfirmMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.ChangeMapMessage import \
    ChangeMapMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.MapInformationsRequestMessage import \
    MapInformationsRequestMessage
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton
from pydofus2.com.ankamagames.jerakine.network.INetworkMessage import \
    INetworkMessage
from pydofus2.com.ankamagames.jerakine.network.ServerConnection import \
    ServerConnection


class ConnectionsHandler(metaclass=Singleton):
    GAME_SERVER: str = "game_server"
    KOLI_SERVER: str = "koli_server"
    CONNECTION_TIMEOUT: int = 3
    MINTIME_BETWEEN_SENDS = 1.2

    def __init__(self):
        self._conn: ServerConnection = None
        self._currentConnectionType: str = ConnectionType.DISCONNECTED
        self._wantedSocketLost: bool = False
        self._wantedSocketLostReason: int = 0
        self.hasReceivedMsg: bool = False
        self.hasReceivedNetworkMsg: bool = False
        self._disconnectMessage = ""
        self._receivedMsgsQueue = Kernel().worker._queue
        self.paused = threading.Event()
        self.resumed = threading.Event()
        self.sendMessageLock = (
            threading.Lock()
        )  # to make sure only one portion of data is being sent at a time throught the socket
        self.last_send_time = None

    @property
    def connectionType(self) -> str:
        return self._currentConnectionType

    @property
    def conn(self) -> ServerConnection:
        return self._conn

    def connectToLoginServer(self, host: str, port: int) -> None:
        Logger().debug("Connecting to login server ...")
        self.etablishConnection(host, port, ConnectionType.TO_LOGIN_SERVER)
        self._currentConnectionType = ConnectionType.TO_LOGIN_SERVER

    def connectToGameServer(self, host: str, port: int) -> None:
        self.etablishConnection(host, port, ConnectionType.TO_GAME_SERVER)
        self._currentConnectionType = ConnectionType.TO_GAME_SERVER
        PlayerManager().gameServerPort = port

    def restart(self) -> None:
        self.closeConnection(DisconnectionReasonEnum.RESTARTING)

    def handleDisconnection(self) -> DisconnectionReason:
        reason: DisconnectionReason = DisconnectionReason(
            self._wantedSocketLost,
            self._wantedSocketLostReason,
            self._disconnectMessage,
        )
        self._wantedSocketLost = False
        self._wantedSocketLostReason = DisconnectionReasonEnum.UNEXPECTED
        self._disconnectMessage = ""
        return reason

    def closeConnection(self, reason: DisconnectionReasonEnum, message: str = ""):
        Logger().debug(f"Close connection : {reason.name}, {message}")
        self._wantedSocketLostReason = reason
        self._wantedSocketLost = True
        self._disconnectMessage = message
        if Kernel().worker.contains("HandshakeFrame"):
            Kernel().worker.removeFrameByName("HandshakeFrame")
        if self.conn.open:
            self.conn.close()
            self.conn.join()
        if self._currentConnectionType == ConnectionType.TO_GAME_SERVER:
            for instId, inst in Kernel.getInstances():
                if inst != Kernel():
                    inst.worker.process(
                        PlayerDisconnectedMessage(
                            threading.currentThread().name, self._currentConnectionType
                        )
                    )
        self._currentConnectionType = ConnectionType.DISCONNECTED

    def etablishConnection(self, host: str, port: int, id: str) -> None:
        from pydofus2.com.ankamagames.dofus.logic.connection.frames.HandshakeFrame import \
            HandshakeFrame

        self._conn = ServerConnection(id, self._receivedMsgsQueue)
        Kernel().worker.addFrame(HandshakeFrame())
        self._conn.start()
        self._conn.connect(host, port)

    def send(self, msg: INetworkMessage) -> None:
        with self.sendMessageLock:
            if not self._conn:
                return Logger().warning(
                    f"Can't send message when no connection is established!, maybe we are shuting down?"
                )
            if type(msg) not in [
                GameMapMovementConfirmMessage,
                GameActionAcknowledgementMessage,
                GameFightTurnFinishMessage,
                GameFightTurnReadyMessage,
                MapInformationsRequestMessage,
                ChangeMapMessage
            ]:
                if self.last_send_time is not None:
                    minNextSendTime = (
                        self.last_send_time + 0.1 + abs(random.gauss(0, 0.3))
                    )
                    diff = minNextSendTime - perf_counter()
                    if diff > 0:
                        Kernel().worker.terminated.wait(diff)
            self.last_send_time = perf_counter()
            self._conn.send(msg)

    def inGameServer(self):
        return self._currentConnectionType == ConnectionType.TO_GAME_SERVER
