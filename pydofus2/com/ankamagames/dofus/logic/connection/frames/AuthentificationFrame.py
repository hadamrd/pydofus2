import base64
import hashlib
import random
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager, KernelEvts
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from pydofus2.com.ankamagames.dofus.kernel.net.DisconnectionReasonEnum import (
    DisconnectionReasonEnum,
)
from pydofus2.com.ankamagames.dofus.logic.connection.actions.LoginValidationAction import (
    LoginValidationAction,
)
import pydofus2.com.ankamagames.dofus.logic.connection.frames.ServerSelectionFrame as ssfrm
from pydofus2.com.ankamagames.dofus.logic.connection.managers.AuthentificationManager import (
    AuthentificationManager,
)
from pydofus2.com.ankamagames.dofus.logic.common.managers.InterClientManager import (
    InterClientManager,
)
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import PlayerManager
from pydofus2.com.ankamagames.dofus.network.enums.IdentificationFailureReasonsEnum import (
    IdentificationFailureReasonEnum,
)
from pydofus2.com.ankamagames.dofus.network.messages.connection.HelloConnectMessage import (
    HelloConnectMessage,
)
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
from pydofus2.com.ankamagames.dofus.network.messages.security.ClientKeyMessage import (
    ClientKeyMessage,
)
from pydofus2.com.ankamagames.jerakine.data.XmlConfig import XmlConfig
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.network.messages.ServerConnectionFailedMessage import (
    ServerConnectionFailedMessage,
)
from pydofus2.com.ankamagames.jerakine.types.DataStoreType import DataStoreType
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority
logger = Logger("Dofus2")


class AuthentificationFrame(Frame):
    HIDDEN_PORT: int = 443
    CONNEXION_MODULE_NAME: str = "ComputerModule_Ankama_Connection"

    def __init__(self) -> None:
        super().__init__()
        self._lastTicket: str
        self._connexionHosts: list = []
        self._dispatchModuleHook: bool = False
        self._connexionSequence: list
        self._lastLoginHash: str = None
        self._currentLogIsForced: bool = False

    @property
    def priority(self) -> int:
        return Priority.NORMAL

    def handleConnectionOpened(self) -> None:
        pass

    def handleConnectionClosed(self) -> None:
        pass

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
            hcmsg = msg
            AuthentificationManager().setPublicKey(hcmsg.key)
            AuthentificationManager().setSalt(hcmsg.salt)
            AuthentificationManager().initAESKey()
            iMsg = AuthentificationManager().getIdentificationMessage()
            self._currentLogIsForced = isinstance(iMsg, IdentificationAccountForceMessage)
            ConnectionsHandler().conn.send(iMsg)
            if InterClientManager.flashKey:
                flashKeyMsg = ClientKeyMessage()
                flashKeyMsg.key = InterClientManager.flashKey
                ConnectionsHandler().conn.send(flashKeyMsg)
            KernelEventsManager().send(KernelEvts.IN_GAME, msg)
            return True

        elif isinstance(msg, IdentificationSuccessMessage):
            ismsg = msg
            if isinstance(ismsg, IdentificationSuccessWithLoginTokenMessage):
                AuthentificationManager().nextToken = IdentificationSuccessWithLoginTokenMessage(ismsg).loginToken
            if ismsg.login:
                AuthentificationManager().username = ismsg.login
            PlayerManager().accountId = ismsg.accountId
            PlayerManager().communityId = ismsg.communityId
            PlayerManager().hasRights = ismsg.hasRights
            PlayerManager().hasConsoleRight = ismsg.hasConsoleRight
            PlayerManager().nickname = ismsg.accountTag.nickname
            PlayerManager().tag = ismsg.accountTag.tagNumber
            PlayerManager().subscriptionEndDate = ismsg.subscriptionEndDate
            PlayerManager().accountCreation = ismsg.accountCreation
            PlayerManager().wasAlreadyConnected = ismsg.wasAlreadyConnected
            DataStoreType.ACCOUNT_ID = str(ismsg.accountId)
            KernelEventsManager().send(KernelEvts.LOGGED_IN, ismsg)
            Kernel().worker.removeFrame(self)
            Kernel().worker.addFrame(ssfrm.ServerSelectionFrame())
            return True

        elif isinstance(msg, IdentificationFailedMessage):
            reasonName = IdentificationFailureReasonEnum(msg.reason).name
            PlayerManager().destroy()
            ConnectionsHandler().closeConnection(
                DisconnectionReasonEnum.EXCEPTION_THROWN, 
                f"Identification failed for reason : {reasonName}"
            )
            if not self._dispatchModuleHook:
                self._dispatchModuleHook = True
                self.pushed()
            return True

        elif isinstance(msg, LoginValidationAction):
            lva = msg
            self._lastLoginHash = hashlib.md5(lva.username.encode("utf-8")).hexdigest()
            connexionPorts = [int(_) for _ in XmlConfig().getEntry("config.connection.port").split(",")]
            connectionHostsEntry = XmlConfig().getEntry("config.connection.host")
            connexionHosts = (
                [lva.host]
                if lva.host
                else (self._connexionHosts if len(self._connexionHosts) > 0 else connectionHostsEntry.split(","))
            )
            self._connexionHosts = connexionHosts
            tmpHosts = []
            for tmpHost in connexionHosts:
                tmpHosts.append({"host": tmpHost, "random": random.random()})
            tmpHosts.sort(key=lambda e: e["random"])
            connexionHosts = []
            for randomHost in tmpHosts:
                connexionHosts.append(randomHost["host"])
            defaultPort = self.HIDDEN_PORT
            self._connexionSequence = list()
            firstConnexionSequence = list()
            for host in connexionHosts:
                for port in connexionPorts:
                    if defaultPort == port:
                        firstConnexionSequence.append({"host": host, "port": port})
                    else:
                        self._connexionSequence.append({"host": host, "port": port})
            if self.HIDDEN_PORT not in connexionPorts:
                for host in connexionHosts:
                    self._connexionSequence.append({"host": host, "port": self.HIDDEN_PORT})
            self._connexionSequence = firstConnexionSequence + self._connexionSequence
            AuthentificationManager().loginValidationAction = lva
            connInfo = self._connexionSequence.pop(0)
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
                        DisconnectionReasonEnum.EXCEPTION_THROWN, 
                        DisconnectionReasonEnum.UNEXPECTED.name
                    )
            return True

    def pushed(self) -> bool:
        logger.debug("[Auth] LoginFrame started")
        return True

    def pulled(self) -> bool:
        logger.debug("[Auth] LoginFrame finished")
        return True
