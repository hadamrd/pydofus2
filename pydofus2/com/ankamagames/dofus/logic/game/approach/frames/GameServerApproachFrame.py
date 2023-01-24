from datetime import datetime
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager, KernelEvts
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.common.frames.QuestFrame import QuestFrame
from pydofus2.com.ankamagames.dofus.logic.game.common.frames.AveragePricesFrame import AveragePricesFrame
from pydofus2.com.ankamagames.dofus.logic.game.common.frames.InventoryManagementFrame import InventoryManagementFrame
from pydofus2.com.ankamagames.dofus.logic.game.common.frames.JobsFrame import JobsFrame
from pydofus2.com.ankamagames.dofus.logic.game.common.frames.SpellInventoryManagementFrame import SpellInventoryManagementFrame
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.FeatureManager import FeatureManager
from pydofus2.com.ankamagames.dofus.network.enums.GameServerTypeEnum import GameServerTypeEnum
from pydofus2.com.ankamagames.jerakine.benchmark.BenchmarkTimer import BenchmarkTimer
import time
from pydofus2.com.ankamagames.dofus.internalDatacenter.connection.BasicCharacterWrapper import (
    BasicCharacterWrapper,
)
from pydofus2.com.ankamagames.dofus.internalDatacenter.items.ItemWrapper import ItemWrapper
import pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler as connh
from pydofus2.com.ankamagames.dofus.logic.connection.managers.AuthentificationManager import (
    AuthentificationManager,
)
from pydofus2.com.ankamagames.dofus.logic.common.managers.InterClientManager import (
    InterClientManager,
)
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import PlayerManager
from pydofus2.com.ankamagames.dofus.logic.game.approach.actions.CharacterSelectionAction import (
    CharacterSelectionAction,
)
from pydofus2.com.ankamagames.dofus.logic.game.common.actions.chat.PopupWarningCloseRequestAction import (
    PopupWarningCloseRequestAction,
)
from pydofus2.com.ankamagames.dofus.logic.game.common.frames.ContextChangeFrame import (
    ContextChangeFrame,
)
from pydofus2.com.ankamagames.dofus.logic.game.common.frames.SynchronisationFrame import (
    SynchronisationFrame,
)
from pydofus2.com.ankamagames.dofus.logic.game.common.frames.WorldFrame import WorldFrame
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import (
    PlayedCharacterManager,
)
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.TimerManager import TimeManager
from pydofus2.com.ankamagames.dofus.network.messages.game.approach.AccountCapabilitiesMessage import (
    AccountCapabilitiesMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.approach.AlreadyConnectedMessage import (
    AlreadyConnectedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.approach.AuthenticationTicketAcceptedMessage import (
    AuthenticationTicketAcceptedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.approach.AuthenticationTicketMessage import (
    AuthenticationTicketMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.approach.AuthenticationTicketRefusedMessage import (
    AuthenticationTicketRefusedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.approach.HelloGameMessage import (
    HelloGameMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.basic.BasicTimeMessage import (
    BasicTimeMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.character.choice.CharacterSelectedForceMessage import (
    CharacterSelectedForceMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.character.choice.CharacterSelectedForceReadyMessage import (
    CharacterSelectedForceReadyMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.character.choice.CharacterSelectedSuccessMessage import (
    CharacterSelectedSuccessMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.character.choice.CharacterSelectionMessage import (
    CharacterSelectionMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.character.choice.CharactersListErrorMessage import (
    CharactersListErrorMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.character.choice.CharactersListMessage import (
    CharactersListMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.character.choice.CharactersListRequestMessage import (
    CharactersListRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameContextCreateRequestMessage import (
    GameContextCreateRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.moderation.PopupWarningCloseRequestMessage import (
    PopupWarningCloseRequestMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.moderation.PopupWarningClosedMessage import (
    PopupWarningClosedMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.startup.StartupActionsListMessage import (
    StartupActionsListMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.security.ClientKeyMessage import (
    ClientKeyMessage,
)
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.ConnectionResumedMessage import (
    ConnectionResumedMessage,
)
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage
from pydofus2.com.ankamagames.jerakine.network.messages.ServerConnectionFailedMessage import (
    ServerConnectionFailedMessage,
)
from pydofus2.com.ankamagames.jerakine.types.DataStoreType import DataStoreType
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority

logger = Logger()


class GameServerApproachFrame(Frame):

    LOADING_TIMEOUT: int = 60

    def __init__(self):
        self._charactersList = list[BasicCharacterWrapper]()
        self._giftList = []
        self._charaListMinusDeadPeople = []
        self._cssmsg = None
        self.authenticationTicketAccepted = False
        self._charactersList = list[BasicCharacterWrapper]()
        self._waitingMessages = list[NetworkMessage]()
        self._requestedCharacterId = None
        self._loadingStart = False
        self._reconnectMsgSend = False

        super().__init__()

    @property
    def priority(self) -> int:
        return Priority.NORMAL

    @property
    def giftList(self) -> list:
        return self._giftList

    @property
    def charaListMinusDeadPeople(self) -> list:
        return self._charaListMinusDeadPeople

    @property
    def requestedCharaId(self) -> float:
        return self._requestedCharacterId

    @requestedCharaId.setter
    def requestedCharaId(self, id: float) -> None:
        self._requestedCharacterId = id

    def isCharacterWaitingForChange(self, id: float) -> bool:
        if self._charactersToRemodelList.get(id):
            return True
        return False

    def process(self, msg: Message) -> bool:

        if isinstance(msg, HelloGameMessage):
            self.authenticationTicketAccepted = False
            atmsg = AuthenticationTicketMessage()
            atmsg.init("fr", AuthentificationManager().gameServerTicket)
            connh.ConnectionsHandler().conn.send(atmsg)
            return True

        elif isinstance(msg, AuthenticationTicketAcceptedMessage):
            BenchmarkTimer(0.5, self.requestCharactersList).start()
            self.authenticationTicketAccepted = True
            return True

        elif isinstance(msg, AuthenticationTicketRefusedMessage):
            self.authenticationTicketAccepted = False
            return True

        elif isinstance(msg, CharactersListMessage):
            clmsg = msg
            self._charactersList = clmsg.characters
            server = PlayerManager().server;
            if FeatureManager().isFeatureWithKeywordEnabled("server.heroic") or server.gameTypeId == GameServerTypeEnum.SERVER_TYPE_EPIC:
                for chi in clmsg.characters:
                    if chi.deathMaxLevel > chi.level:
                        bonusXp = 6
                    else:
                        bonusXp = 3
                    o = BasicCharacterWrapper.create(chi.id,chi.name,chi.level,chi.entityLook,chi.breed,chi.sex,chi.deathState,chi.deathCount,chi.deathMaxLevel,bonusXp,False);
                    PlayerManager().charactersList.append(o)
            else:
                bonusXpFeatureActivated = FeatureManager().isFeatureWithKeywordEnabled("character.xp.bonusForYoungerCharacters")
                for cbi in clmsg.characters:
                    bonusXp = 1
                    if bonusXpFeatureActivated:
                        for cbi2 in clmsg.characters:
                            if cbi2.id != cbi.id and cbi2.level > cbi.level and bonusXp < 4: 
                                bonusXp += 1
                    o = BasicCharacterWrapper.create(cbi.id,cbi.name,cbi.level,cbi.entityLook,cbi.breed,cbi.sex,0,0,0,bonusXp, False)
                    PlayerManager().charactersList.append(o)
            KernelEventsManager().send(KernelEvts.CHARACTERS_LIST, return_value=PlayerManager().charactersList)
            if PlayerManager().allowAutoConnectCharacter:
                characterId = PlayerManager().autoConnectOfASpecificCharacterId
                Kernel().worker.process(CharacterSelectionAction.create(characterId, False))
            return False

        elif isinstance(msg, ServerConnectionFailedMessage):
            scfMsg = ServerConnectionFailedMessage(msg)
            self.authenticationTicketAccepted = False
            if scfMsg.failedConnection == connh.ConnectionsHandler().conn.getSubConnection(scfMsg):
                PlayerManager().destroy()
            return True

        elif isinstance(msg, AlreadyConnectedMessage):
            PlayerManager().wasAlreadyConnected = True
            return True

        elif isinstance(msg, CharactersListErrorMessage):
            return False

        elif isinstance(msg, AccountCapabilitiesMessage):
            accmsg = msg
            PlayerManager().adminStatus = accmsg.status
            PlayerManager().canCreateNewCharacter = accmsg.canCreateNewCharacter
            return True

        elif isinstance(msg, CharacterSelectedSuccessMessage):
            import pydofus2.com.ankamagames.dofus.logic.game.common.frames.PlayedCharacterUpdatesFrame as pcuF

            cssmsg = msg
            self._loadingStart = time.perf_counter()
            if Kernel().worker.getFrame("ServerSelectionFrame"):
                Kernel().worker.removeFrameByName("ServerSelectionFrame")
            PlayedCharacterManager().infos = cssmsg.infos
            DataStoreType.CHARACTER_ID = str(cssmsg.infos.id)
            Kernel().worker.addFrame(WorldFrame())
            Kernel().worker.addFrame(SynchronisationFrame())
            Kernel().worker.addFrame(pcuF.PlayedCharacterUpdatesFrame())
            Kernel().worker.addFrame(SpellInventoryManagementFrame())
            Kernel().worker.addFrame(InventoryManagementFrame())
            Kernel().worker.addFrame(ContextChangeFrame())
            Kernel().worker.addFrame(JobsFrame())
            Kernel().worker.addFrame(QuestFrame())
            Kernel().worker.addFrame(AveragePricesFrame())
            KernelEventsManager().send(KernelEvts.CHARACTER_SELECTION_SUCCESS, return_value=cssmsg.infos)
            if Kernel().beingInReconection and not self._reconnectMsgSend:
                self._reconnectMsgSend = True
                connh.ConnectionsHandler().conn.send(CharacterSelectedForceReadyMessage())
            if InterClientManager.flashKey and (
                not PlayerManager() or PlayerManager().server.id != 129 and PlayerManager().server.id != 130
            ):
                flashKeyMsg = ClientKeyMessage()
                flashKeyMsg.init(InterClientManager.flashKey)
                connh.ConnectionsHandler().conn.send(flashKeyMsg)
            self._cssmsg = cssmsg
            PlayedCharacterManager().infos = self._cssmsg.infos
            DataStoreType.CHARACTER_ID = str(self._cssmsg.infos.id)
            Kernel().worker.removeFrame(self)
            gccrmsg = GameContextCreateRequestMessage()
            connh.ConnectionsHandler().conn.send(gccrmsg)
            now = time.perf_counter()
            delta = now - self._loadingStart
            if delta > self.LOADING_TIMEOUT:
                logger.warn(f"Client took too long to load ({delta}s).")
            return True

        elif isinstance(msg, ConnectionResumedMessage):
            return True

        elif isinstance(msg, CharacterSelectedForceMessage):
            if not self._reconnectMsgSend:
                Kernel().beingInReconection = True
                self.characterId = msg.id
                self._reconnectMsgSend = True
                connh.ConnectionsHandler().conn.send(CharacterSelectedForceReadyMessage())

        elif isinstance(msg, BasicTimeMessage):
            btmsg = msg
            TimeManager().serverTimeLag = (
                btmsg.timestamp + btmsg.timezoneOffset * 60 * 1000 - datetime.now().timestamp()
            )
            TimeManager().serverUtcTimeLag = btmsg.timestamp - datetime.now().timestamp()
            TimeManager().timezoneOffset = btmsg.timezoneOffset * 60 * 1000
            TimeManager().dofusTimeYearLag = -1370
            return True

        elif isinstance(msg, StartupActionsListMessage):
            salm = msg
            self._giftList = []
            for gift in salm.actions:
                _items = []
                for item in gift.items:
                    iw = ItemWrapper.create(0, 0, item.objectGID, item.quantity, item.effects, False)
                    _items.append(iw)
                    oj = {
                        "uid": gift.uid,
                        "title": gift.title,
                        "text": gift.text,
                        "items": _items,
                    }
                self._giftList.append(oj)
            if len(self._giftList):
                self._charaListMinusDeadPeople = []
                for perso in self._charactersList:
                    if not perso.deathState or perso.deathState == 0:
                        self._charaListMinusDeadPeople.append(perso)
            else:
                Kernel().worker.removeFrame(self)
                logger.warn("Empty Gift List Received")
            return True

        elif isinstance(msg, PopupWarningClosedMessage):
            return True

        elif isinstance(msg, PopupWarningCloseRequestAction):
            pwcrmsg = PopupWarningCloseRequestMessage()
            connh.ConnectionsHandler().conn.send(pwcrmsg)
            return True

        elif isinstance(msg, CharacterSelectionAction):
            characterId = msg.characterId
            self._requestedCharacterId = characterId
            self._requestedToRemodelCharacterId = 0
            csmsg = CharacterSelectionMessage()
            csmsg.init(id_=characterId)
            connh.ConnectionsHandler().conn.send(csmsg)
            return True

        return False

    def pulled(self) -> bool:
        return True

    def pushed(self) -> bool:
        return True

    def requestCharactersList(self) -> None:
        clrmsg: CharactersListRequestMessage = CharactersListRequestMessage()
        if connh.ConnectionsHandler().conn:
            connh.ConnectionsHandler().conn.send(clrmsg)
