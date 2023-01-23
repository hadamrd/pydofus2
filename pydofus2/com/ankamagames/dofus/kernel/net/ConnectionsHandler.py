import pydofus2.com.ankamagames.dofus.kernel.Kernel as krnl
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionType import ConnectionType
from pydofus2.com.ankamagames.dofus.kernel.net.DisconnectionReason import DisconnectionReason
from pydofus2.com.ankamagames.dofus.kernel.net.DisconnectionReasonEnum import DisconnectionReasonEnum
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import PlayerManager
from pydofus2.com.ankamagames.dofus.logic.connection.frames.HandshakeFrame import HandshakeFrame
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.ConnectionResumedMessage import ConnectionResumedMessage
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton
from pydofus2.com.ankamagames.jerakine.network.ServerConnection import ServerConnection

logger = Logger("Dofus2")


class ConnectionsHandler(metaclass=Singleton):
    
    GAME_SERVER: str = "game_server"
    KOLI_SERVER: str = "koli_server"
    CONNECTION_TIMEOUT: int = 3

    def __init__(self):
        self._conn: ServerConnection = None
        self._currentConnectionType: str = None
        self._wantedSocketLost: bool = False
        self._wantedSocketLostReason: int = 0
        self._hasReceivedMsg: bool = False
        self._hasReceivedNetworkMsg: bool = False
        self._disconnectMessage = ""

    @property
    def connectionType(self) -> str:
        return self._currentConnectionType

    @property
    def hasReceivedMsg(self) -> bool:
        return self._hasReceivedMsg

    @hasReceivedMsg.setter
    def hasReceivedMsg(self, value: bool) -> None:
        self._hasReceivedMsg = value

    @property
    def hasReceivedNetworkMsg(self) -> bool:
        return self._hasReceivedNetworkMsg

    @hasReceivedNetworkMsg.setter
    def hasReceivedNetworkMsg(self, value: bool) -> None:
        self._hasReceivedNetworkMsg = value

    @property
    def conn(self) -> ServerConnection:
        return self._conn

    def connectToLoginServer(self, host: str, port: int) -> None:
        self.closeConnection()
        self.etablishConnection(host, port, ConnectionType.TO_LOGIN_SERVER)
        self._currentConnectionType = ConnectionType.TO_LOGIN_SERVER

    def connectToGameServer(self, gameServerHost: str, gameServerPort: int) -> None:
        self.closeConnection()
        self.etablishConnection(gameServerHost, gameServerPort, ConnectionType.TO_GAME_SERVER)
        self._currentConnectionType = ConnectionType.TO_GAME_SERVER
        PlayerManager().gameServerPort = gameServerPort

    def closeConnection(self) -> None:
        logger.debug("[Connhandler] Want to close curr connection")
        if self.conn:
            if krnl.Kernel().getWorker().contains("HandshakeFrame"):
                krnl.Kernel().getWorker().removeFrame(krnl.Kernel().getWorker().getFrame("HandshakeFrame"))
            if self.conn.connected:
                self._conn.close()
                self._conn.finished.wait()
                self._conn.kill()
            self._currentConnectionType = ConnectionType.DISCONNECTED

    def handleDisconnection(self) -> DisconnectionReason:
        self.closeConnection()
        reason: DisconnectionReason = DisconnectionReason(
            self._wantedSocketLost, self._wantedSocketLostReason, msg=self._disconnectMessage
        )
        self._wantedSocketLost = False
        self._wantedSocketLostReason = DisconnectionReasonEnum.UNEXPECTED
        return reason

    def connectionGonnaBeClosed(self, expectedReason: DisconnectionReasonEnum, msg: str = "") -> None:
        self._wantedSocketLostReason = expectedReason
        self._wantedSocketLost = True
        self._disconnectMessage = msg
        self._conn.expectConnectionClose(expectedReason, msg)

    def pause(self) -> None:
        logger.info("Pause connection")
        self._conn.pause()

    def resume(self) -> None:
        logger.info("Resume connection")
        if self._conn:
            self._conn.resume()
        krnl.Kernel().getWorker().process(ConnectionResumedMessage())
        
    def etablishConnection(self, host: str, port: int, id: str) -> None:
        self._conn = ServerConnection(id)
        krnl.Kernel().getWorker().addFrame(HandshakeFrame())
        self._conn.start()
        self._conn.connect(host, port)
        logger.debug(f"Connection process pid: {self._conn.pid}")
