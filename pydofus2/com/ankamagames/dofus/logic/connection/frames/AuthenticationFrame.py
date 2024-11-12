from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from pydofus2.com.ankamagames.dofus.kernel.net.DisconnectionReasonEnum import DisconnectionReasonEnum
from pydofus2.com.ankamagames.dofus.logic.common.frames.CharacterFrame import CharacterFrame
from pydofus2.com.ankamagames.dofus.logic.common.managers.InterClientManager import InterClientManager
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import PlayerManager
from pydofus2.com.ankamagames.dofus.logic.connection.actions.LoginValidationAction import LoginValidationAction
from pydofus2.com.ankamagames.dofus.logic.connection.frames.ServerSelectionFrame import ServerSelectionFrame
from pydofus2.com.ankamagames.dofus.logic.connection.managers.AuthenticationManager import AuthenticationManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.TimeManager import TimeManager
from pydofus2.com.ankamagames.dofus.network.enums.IdentificationFailureReasonsEnum import (
    IdentificationFailureReasonEnum,
)
from pydofus2.com.ankamagames.dofus.network.messages.connection.HelloConnectMessage import HelloConnectMessage
from pydofus2.com.ankamagames.dofus.network.messages.connection.IdentificationAccountForceMessage import (
    IdentificationAccountForceMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.connection.IdentificationFailedMessage import (
    IdentificationFailedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.connection.IdentificationSuccessMessage import (
    IdentificationSuccessMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.connection.IdentificationSuccessWithLoginTokenMessage import (
    IdentificationSuccessWithLoginTokenMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.connection.register.NicknameRegistrationMessage import (
    NicknameRegistrationMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.security.ClientKeyMessage import ClientKeyMessage
from pydofus2.com.ankamagames.jerakine.data.XmlConfig import XmlConfig
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.network.messages.ServerConnectionFailedMessage import (
    ServerConnectionFailedMessage,
)
from pydofus2.com.ankamagames.jerakine.types.DataStoreType import DataStoreType
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority
from pydofus2.com.ClientStatusEnum import ClientStatusEnum


class AuthenticationFrame(Frame):
    HIDDEN_PORT: int = 443
    CONNEXION_MODULE_NAME: str = "ComputerModule_Ankama_Connection"

    def __init__(self) -> None:
        super().__init__()
        self._lastTicket: str
        self._connexionHosts: list = []
        self._dispatchModuleHook: bool = False
        self._connexionSequence: list
        self._currentLogIsForced: bool = False

    @property
    def priority(self) -> int:
        return Priority.NORMAL

    def process(self, msg: Message) -> bool:

        if isinstance(msg, ServerConnectionFailedMessage):
            ConnectionsHandler().conn.stopConnectionTimeout()
            if self._connexionSequence:
                retryConnInfo = self._connexionSequence.pop(0)
                if retryConnInfo:
                    ConnectionsHandler().connectToLoginServer(retryConnInfo.host, retryConnInfo.port)
                else:
                    PlayerManager().destroy()
            return True

        elif isinstance(msg, HelloConnectMessage):
            flashKeyMsg = ClientKeyMessage()
            flashKeyMsg.init(InterClientManager().getFlashKey())
            Logger().info(f"Sending flash key to server: {flashKeyMsg.key}")
            ConnectionsHandler().send(flashKeyMsg)
            AuthenticationManager().setPublicKey(msg.key)
            AuthenticationManager().setSalt(msg.salt)
            AuthenticationManager().initAESKey()
            iMsg = AuthenticationManager().getIdentificationMessage()
            self._currentLogIsForced = isinstance(iMsg, IdentificationAccountForceMessage)
            ConnectionsHandler().send(iMsg)
            KernelEventsManager().send(KernelEvent.ClientStatusUpdate, ClientStatusEnum.AUTHENTICATING_TO_LOGIN_SERVER)
            return True

        elif isinstance(msg, IdentificationSuccessMessage):
            if isinstance(msg, IdentificationSuccessWithLoginTokenMessage):
                AuthenticationManager().nextToken = msg.loginToken
            if msg.login:
                AuthenticationManager().username = msg.login
            PlayerManager().accountId = msg.accountId
            PlayerManager().communityId = msg.communityId
            PlayerManager().hasRights = msg.hasRights
            PlayerManager().hasReportRight = msg.hasReportRight
            PlayerManager().nickname = msg.accountTag.nickname
            PlayerManager().tag = msg.accountTag.tagNumber
            PlayerManager().subscriptionEndDate = msg.subscriptionEndDate
            if PlayerManager().isBasicAccount():
                Logger().info("Player has basic account")
            else:
                date = TimeManager().format_date_irl(msg.subscriptionEndDate, True)
                time = TimeManager().format_clock(msg.subscriptionEndDate, True, True)
                Logger().info(f"Player is subscribed until: {date} {time}")

            PlayerManager().accountCreation = msg.accountCreation
            PlayerManager().wasAlreadyConnected = msg.wasAlreadyConnected
            DataStoreType.ACCOUNT_ID = str(msg.accountId)
            Kernel().worker.removeFrame(self)
            Kernel().worker.addFrame(CharacterFrame())
            Kernel().worker.addFrame(ServerSelectionFrame())
            KernelEventsManager().send(KernelEvent.PlayerLoginSuccess, msg)
            formatted = TimeManager().getFormatterDateFromTime(msg.subscriptionEndDate)
            KernelEventsManager().send(
                KernelEvent.ClientStatusUpdate,
                ClientStatusEnum.AUTHENTICATED_TO_LOGIN_SERVER,
                {"subscribed": not PlayerManager().isBasicAccount(), "subscriptionEndDate": formatted},
            )
            return True

        elif isinstance(msg, NicknameRegistrationMessage):
            KernelEventsManager().send(KernelEvent.ClientCrashed, "Account nickname missing!")

        elif isinstance(msg, IdentificationFailedMessage):
            reason = IdentificationFailureReasonEnum(msg.reason)
            PlayerManager().destroy()
            if reason == IdentificationFailureReasonEnum.BANNED:
                KernelEventsManager().send(KernelEvent.ClientStatusUpdate, ClientStatusEnum.BANNED)
                ConnectionsHandler().closeConnection(
                    DisconnectionReasonEnum.BANNED, f"Identification failed for reason : {reason.name}"
                )
            else:
                KernelEventsManager().send(
                    KernelEvent.ClientStatusUpdate,
                    ClientStatusEnum.FAILED_TO_IDENTIFY,
                    {"identificationFailureReason": reason.name},
                )
                ConnectionsHandler().closeConnection(
                    DisconnectionReasonEnum.EXCEPTION_THROWN, f"Identification failed for reason : {reason.name}"
                )
            return True

        elif isinstance(msg, LoginValidationAction):
            Logger().info(f"Login to server {msg.serverId} called")
            connectionHostsEntry = XmlConfig().getEntry("config.connection.host")
            allHostsInfos = self.parseHosts(connectionHostsEntry)
            Logger().info(f"Hosts infos : {allHostsInfos}")
            hostChosenByUser = msg.host
            if not hostChosenByUser:
                hostChosenByUser, foundHost = self.chooseHost(allHostsInfos)
                if not foundHost:
                    return KernelEventsManager().send(
                        KernelEvent.ClientCrashed, "No selectable host, aborting connection."
                    )
            self.connexionSequence = self.buildConnexionSequence(allHostsInfos, hostChosenByUser)
            AuthenticationManager().loginValidationAction = msg
            connInfo = self.connexionSequence.pop(0)
            Logger().info(f"connInfo: {connInfo}")
            KernelEventsManager().send(
                KernelEvent.ClientStatusUpdate, ClientStatusEnum.CONNECTING_TO_LOGIN_SERVER, connInfo
            )
            ConnectionsHandler().connectToLoginServer(connInfo["host"], connInfo["port"])
            return True

        elif isinstance(msg, ServerConnectionFailedMessage):
            ConnectionsHandler().conn.stopConnectionTimeout()
            if self._connexionSequence:
                retryConnInfo = self._connexionSequence.pop(0)
                if retryConnInfo:
                    ConnectionsHandler().connectToLoginServer(retryConnInfo["host"], retryConnInfo["port"])
                else:
                    PlayerManager().destroy()
                    ConnectionsHandler().closeConnection(
                        DisconnectionReasonEnum.EXCEPTION_THROWN, DisconnectionReasonEnum.UNEXPECTED.name
                    )
            return True

    @classmethod
    def parseHosts(cls, connectionHostsEntry: str):
        allHostsInfos = {}
        for host in connectionHostsEntry.split("|"):
            field = host.split(":")
            if len(field) == 3:
                allHostsInfos[field[0].strip()] = [field[1].strip(), field[2].strip()]
            else:
                Logger().error(f"Connection server has the wrong format. It won't be added to the list: {host}")
        return allHostsInfos

    def chooseHost(self, allHostsInfos: dict):
        for strKey in allHostsInfos:
            return strKey, True
        return None, False

    def buildConnexionSequence(self, allHostsInfos, hostKey):
        connexionSequence = []
        host = allHostsInfos[hostKey]
        hostPorts = host[1].split(",")
        hostName = host[0]
        chosenPort = ""
        for port in hostPorts:
            if port == chosenPort:
                connexionSequence.insert(0, {"host": hostName, "port": int(port)})
            else:
                connexionSequence.append({"host": hostName, "port": int(port)})
        return connexionSequence

    def pushed(self) -> bool:
        Logger().info("Auth frame pushed")
        return True

    def pulled(self) -> bool:
        Logger().info("Auth frame pulled")
        return True
