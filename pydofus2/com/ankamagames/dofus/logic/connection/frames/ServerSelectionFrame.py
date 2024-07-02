from types import FunctionType

from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager
from pydofus2.com.ankamagames.dofus.datacenter.servers.Server import Server
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from pydofus2.com.ankamagames.dofus.kernel.net.DisconnectionReasonEnum import DisconnectionReasonEnum
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import PlayerManager
from pydofus2.com.ankamagames.dofus.logic.connection.actions.LoginValidationWithTokenAction import (
    LoginValidationWithTokenAction,
)
from pydofus2.com.ankamagames.dofus.logic.connection.actions.ServerSelectionAction import ServerSelectionAction
from pydofus2.com.ankamagames.dofus.logic.connection.managers.AuthenticationManager import AuthenticationManager
from pydofus2.com.ankamagames.dofus.network.enums.ServerConnectionErrorEnum import ServerConnectionErrorEnum
from pydofus2.com.ankamagames.dofus.network.enums.ServerStatusEnum import ServerStatusEnum
from pydofus2.com.ankamagames.dofus.network.messages.connection.SelectedServerDataExtendedMessage import (
    SelectedServerDataExtendedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.connection.SelectedServerDataMessage import (
    SelectedServerDataMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.connection.SelectedServerRefusedMessage import (
    SelectedServerRefusedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.connection.ServerSelectionMessage import ServerSelectionMessage
from pydofus2.com.ankamagames.dofus.network.messages.connection.ServersListMessage import ServersListMessage
from pydofus2.com.ankamagames.dofus.network.messages.connection.ServerStatusUpdateMessage import (
    ServerStatusUpdateMessage,
)
from pydofus2.com.ankamagames.dofus.network.types.connection.GameServerInformations import GameServerInformations
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.network.messages.ExpectedSocketClosureMessage import (
    ExpectedSocketClosureMessage,
)
from pydofus2.com.ankamagames.jerakine.network.messages.Worker import Worker
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority
from pydofus2.com.ClientStatusEnum import ClientStatusEnum


class ServerSelectionFrame(Frame):
    def __init__(self):
        self._serversList: list[GameServerInformations] = []
        self._serversUsedList: list[GameServerInformations] = []
        self.selectedServer: SelectedServerDataMessage = None
        self._worker: Worker = None
        self._alreadyConnectedToServerId: int = 0
        self._serverSelectionAction: ServerSelectionAction = None
        self._connectionPorts: list = []
        self._waitingServerOnline = False
        self._serversTypeAvailableSlots = dict()
        super().__init__()

    @property
    def priority(self) -> int:
        return Priority.HIGH

    @property
    def usedServers(self) -> list[GameServerInformations]:
        return self._serversUsedList

    @property
    def servers(self) -> list[GameServerInformations]:
        return self._serversList

    @property
    def availableSlotsByServerType(self) -> list:
        return self._serversTypeAvailableSlots

    def pushed(self) -> bool:
        return True

    def process(self, msg: Message) -> bool:

        if isinstance(msg, ServersListMessage):
            KernelEventsManager().send(KernelEvent.ClientStatusUpdate, ClientStatusEnum.GAME_SERVERS_LIST_RECEIVED)
            slmsg = msg
            PlayerManager().server = None
            self._serversList = slmsg.servers
            self._serversList.sort(key=lambda x: x.date)
            self.broadcastServersListUpdate()
            if AuthenticationManager()._lva and AuthenticationManager()._lva.serverId is not None:
                self.selectServer(AuthenticationManager()._lva.serverId)
            else:
                Logger().warning("No serverId specified in Auth Manager, cannot select any server.")
            return True

        elif isinstance(msg, ServerStatusUpdateMessage):
            serverHasBeenUpdated = False
            for knownServer in self._serversList:
                if msg.server.id == knownServer.id:
                    knownServer.charactersCount = msg.server.charactersCount
                    knownServer.completion = msg.server.completion
                    knownServer.isSelectable = msg.server.isSelectable
                    knownServer.status = msg.server.status
                    serverHasBeenUpdated = True
            if not serverHasBeenUpdated:
                self._serversList.append(msg.server)
                self._serversList.sort(key=lambda x: x.date)
            serverStatus = ServerStatusEnum(msg.server.status)
            Logger().info(f"Server {msg.server.id} status changed to {serverStatus.name}.")
            if self._waitingServerOnline and self._waitingServerOnline == msg.server.id:
                self.selectServer(msg.server.id)
                self._waitingServerOnline = False
            self.broadcastServersListUpdate()
            KernelEventsManager().send(KernelEvent.ServerStatusUpdate, msg.server)
            return True

        elif isinstance(msg, ServerSelectionAction):
            self.selectServer(msg.serverId)
            return True

        elif isinstance(msg, SelectedServerDataExtendedMessage):
            ssdemsg = msg
            self._serversList = ssdemsg.servers
            self._serversList.sort(key=lambda x: x.date)
            self.broadcastServersListUpdate(True)

        elif isinstance(msg, ExpectedSocketClosureMessage):
            from pydofus2.com.ankamagames.dofus.logic.game.approach.frames.GameServerApproachFrame import (
                GameServerApproachFrame,
            )

            if msg.reason == DisconnectionReasonEnum.SWITCHING_TO_GAME_SERVER:
                Kernel().worker.addFrame(GameServerApproachFrame())
                ConnectionsHandler().connectToGameServer(self.selectedServer.address, self.selectedServer.ports[0])
            elif msg.reason == DisconnectionReasonEnum.CHANGING_SERVER:
                if not AuthenticationManager()._lva or AuthenticationManager()._lva.serverId is None:
                    Logger().error(f"Closed connection to change server but no serverId is specified in Auth Manager")
                else:
                    from pydofus2.com.ankamagames.dofus.logic.common.frames.QueueFrame import QueueFrame
                    from pydofus2.com.ankamagames.dofus.logic.connection.frames.AuthenticationFrame import (
                        AuthenticationFrame,
                    )

                    Logger().info(
                        f"Connection closed to change server to {AuthenticationManager()._lva.serverId}, will reconnect"
                    )
                    Kernel().worker.addFrame(AuthenticationFrame())
                    Kernel().worker.addFrame(QueueFrame())
                    Kernel().worker.process(
                        LoginValidationWithTokenAction.create(
                            AuthenticationManager()._lva.serverId != 0, AuthenticationManager()._lva.serverId
                        )
                    )
            return True

        if isinstance(msg, (SelectedServerDataMessage, SelectedServerDataExtendedMessage)):
            KernelEventsManager().send(
                KernelEvent.ClientStatusUpdate, ClientStatusEnum.SERVER_SELECT_SUCCESS, {"serverId": msg.to_json()}
            )
            self.selectedServer = msg
            AuthenticationManager().gameServerTicket = AuthenticationManager().decodeWithAES(msg.ticket).decode()
            PlayerManager().server = Server.getServerById(msg.serverId)
            PlayerManager().kisServerPort = 0
            self._connectionPorts = msg.ports
            KernelEventsManager().send(
                KernelEvent.SelectedServerData,
                msg.serverId,
                msg.address,
                msg.ports,
                msg.canCreateNewCharacter,
                msg.ticket,
            )
            ConnectionsHandler().closeConnection(DisconnectionReasonEnum.SWITCHING_TO_GAME_SERVER)
            KernelEventsManager().send(KernelEvent.ClientStatusUpdate, ClientStatusEnum.SWITCHING_TO_GAME_SERVER)
            return True

        if isinstance(msg, SelectedServerRefusedMessage):
            for server in self._serversList:
                self.getUpdateServerStatusFunction(msg.serverId, msg.serverStatus)(server)
            self.broadcastServersListUpdate()
            error_text = self.getSelectionErrorText(msg.error, msg.serverStatus)
            KernelEventsManager().send(
                KernelEvent.SelectedServerRefused,
                msg.serverId,
                msg.error,
                msg.serverStatus,
                error_text,
                self.getSelectableServers(),
            )
            return True

    def pulled(self) -> bool:
        self._serversList = None
        self._serversUsedList = None
        self._worker = None
        return True

    def getSelectableServers(self) -> list:
        selectableServers = list()
        for server in self._serversList:
            if server.status == ServerStatusEnum.ONLINE and server.isSelectable:
                selectableServers.append(server.id)
        return selectableServers

    def broadcastServersListUpdate(self, silent: bool = False) -> None:
        self._serversTypeAvailableSlots = dict()
        self._serversUsedList = list[GameServerInformations]()
        PlayerManager().serversList = list[int]()
        for server in self._serversList:
            if server.type not in self._serversTypeAvailableSlots:
                self._serversTypeAvailableSlots[server.type] = 0
            if server.charactersCount < server.charactersSlots:
                self._serversTypeAvailableSlots[server.type] += 1
            if server.charactersCount > 0:
                self._serversUsedList.append(server)
                PlayerManager().serversList.append(server.id)
        KernelEventsManager().send(
            KernelEvent.ServersList, self._serversList, self._serversUsedList, self._serversTypeAvailableSlots
        )

    def getSelectionErrorText(self, error_type, server_status):
        error_text = ""
        server_status = ServerStatusEnum(server_status)
        if error_type == ServerConnectionErrorEnum.SERVER_CONNECTION_ERROR_DUE_TO_STATUS:
            error_text = "Status is "
            if server_status == ServerStatusEnum.OFFLINE:
                error_text += "Offline"
            elif server_status == ServerStatusEnum.STARTING:
                error_text += "Starting"
            elif server_status == ServerStatusEnum.NOJOIN:
                error_text += "Nojoin"
            elif server_status == ServerStatusEnum.SAVING:
                error_text += "Saving"
            elif server_status == ServerStatusEnum.STOPING:
                error_text += "Stoping"
            elif server_status == ServerStatusEnum.FULL:
                error_text += "Full"
            elif server_status == ServerStatusEnum.STATUS_UNKNOWN:
                error_text += "Unknown"
        elif error_type == ServerConnectionErrorEnum.SERVER_CONNECTION_ERROR_SUBSCRIBERS_ONLY:
            error_text = "SubscribersOnly"
        elif error_type == ServerConnectionErrorEnum.SERVER_CONNECTION_ERROR_REGULAR_PLAYERS_ONLY:
            error_text = "RegularPlayersOnly"
        elif error_type == ServerConnectionErrorEnum.SERVER_CONNECTION_ERROR_MONOACCOUNT_CANNOT_VERIFY:
            error_text = "MonoaccountCannotVerify"
        elif error_type == ServerConnectionErrorEnum.SERVER_CONNECTION_ERROR_MONOACCOUNT_ONLY:
            error_text = "MonoaccountOnly"
        else:  # Default case
            error_text = "NoReason"
        return error_text

    def getUpdateServerStatusFunction(self, serverId: int, newStatus: int) -> FunctionType:
        def function(
            element: GameServerInformations,
            index: int = None,
            arr: list[GameServerInformations] = None,
        ) -> None:
            if serverId == element.id:
                element.status = newStatus

        return function

    def requestServerSelection(self, serverId: int) -> None:
        ssmsg = ServerSelectionMessage()
        ssmsg.init(serverId)
        ConnectionsHandler().send(ssmsg)

    def getSelectedServerInformations(self) -> GameServerInformations:
        for server in self._serversList:
            if server.id == self.selectedServer.serverId:
                return server

    def selectServer(self, serverId: int) -> None:
        if self._alreadyConnectedToServerId and self._alreadyConnectedToServerId == serverId:
            Logger().warning(f"Already connected to server {self._alreadyConnectedToServerId}.")
            return

        if self._alreadyConnectedToServerId > 0 and serverId != self._alreadyConnectedToServerId:
            self._serverSelectionAction = ServerSelectionAction.create(serverId)
            self.serverAlreadyInName = Server.getServerById(self._alreadyConnectedToServerId).name
            self.serverSelectedName = Server.getServerById(serverId).name

        for server in self._serversList:
            if str(server.id) == str(serverId):
                if ServerStatusEnum(server.status) == ServerStatusEnum.ONLINE:
                    self.requestServerSelection(server.id)
                    KernelEventsManager().send(
                        KernelEvent.ClientStatusUpdate, ClientStatusEnum.SELECTING_SERVER, {"serverId": server.id}
                    )
                    return
                elif ServerStatusEnum(server.status) == ServerStatusEnum.SAVING:
                    self._waitingServerOnline = server.id
                    Logger().info(f"Server {server.id} is saving, waiting for it to be online.")
                else:
                    err_type = ServerConnectionErrorEnum.SERVER_CONNECTION_ERROR_DUE_TO_STATUS
                    error_text = self.getSelectionErrorText(err_type, server.status)
                    KernelEventsManager().send(
                        KernelEvent.SelectedServerRefused,
                        server.id,
                        err_type,
                        server.status,
                        error_text,
                        self.getSelectableServers(),
                    )
                    KernelEventsManager().send(
                        KernelEvent.ClientStatusUpdate,
                        ClientStatusEnum.SERVER_SELECTION_IMPOSSIBLE,
                        {"serverId": server.id, "error": error_text},
                    )
