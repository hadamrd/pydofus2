import time
from datetime import datetime

from prettytable import PrettyTable

from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import \
    KernelEventsManager
from pydofus2.com.ankamagames.dofus.internalDatacenter.connection.BasicCharacterWrapper import \
    BasicCharacterWrapper
from pydofus2.com.ankamagames.dofus.internalDatacenter.items.ItemWrapper import \
    ItemWrapper
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import \
    ConnectionsHandler
from pydofus2.com.ankamagames.dofus.logic.common.frames.AlignmentFrame import \
    AlignmentFrame
from pydofus2.com.ankamagames.dofus.logic.common.frames.MiscFrame import \
    MiscFrame
from pydofus2.com.ankamagames.dofus.logic.common.frames.NpcFrame import \
    NpcFrame
from pydofus2.com.ankamagames.dofus.logic.common.frames.QuestFrame import \
    QuestFrame
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import \
    PlayerManager
from pydofus2.com.ankamagames.dofus.logic.connection.managers.AuthentificationManager import \
    AuthentificationManager
from pydofus2.com.ankamagames.dofus.logic.game.approach.actions.CharacterSelectionAction import \
    CharacterSelectionAction
from pydofus2.com.ankamagames.dofus.logic.game.common.actions.chat.PopupWarningCloseRequestAction import \
    PopupWarningCloseRequestAction
from pydofus2.com.ankamagames.dofus.logic.game.common.frames.AveragePricesFrame import \
    AveragePricesFrame
from pydofus2.com.ankamagames.dofus.logic.game.common.frames.ContextChangeFrame import \
    ContextChangeFrame
from pydofus2.com.ankamagames.dofus.logic.game.common.frames.InventoryManagementFrame import \
    InventoryManagementFrame
from pydofus2.com.ankamagames.dofus.logic.game.common.frames.JobsFrame import \
    JobsFrame
from pydofus2.com.ankamagames.dofus.logic.game.common.frames.MountFrame import \
    MountFrame
from pydofus2.com.ankamagames.dofus.logic.game.common.frames.SocialFrame import \
    SocialFrame
from pydofus2.com.ankamagames.dofus.logic.game.common.frames.SpellInventoryManagementFrame import \
    SpellInventoryManagementFrame
from pydofus2.com.ankamagames.dofus.logic.game.common.frames.SynchronisationFrame import \
    SynchronisationFrame
from pydofus2.com.ankamagames.dofus.logic.game.common.frames.WorldFrame import \
    WorldFrame
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.FeatureManager import \
    FeatureManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.InactivityManager import \
    InactivityManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import \
    PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.TimeManager import \
    TimeManager
from pydofus2.com.ankamagames.dofus.logic.game.roleplay.frames.PartyFrame import \
    PartyFrame
from pydofus2.com.ankamagames.dofus.network.enums.GameServerTypeEnum import \
    GameServerTypeEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.approach.AccountCapabilitiesMessage import \
    AccountCapabilitiesMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.approach.AlreadyConnectedMessage import \
    AlreadyConnectedMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.approach.AuthenticationTicketAcceptedMessage import \
    AuthenticationTicketAcceptedMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.approach.AuthenticationTicketMessage import \
    AuthenticationTicketMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.approach.AuthenticationTicketRefusedMessage import \
    AuthenticationTicketRefusedMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.approach.HelloGameMessage import \
    HelloGameMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.basic.BasicTimeMessage import \
    BasicTimeMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.character.choice.CharacterFirstSelectionMessage import \
    CharacterFirstSelectionMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.character.choice.CharacterSelectedErrorMessage import \
    CharacterSelectedErrorMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.character.choice.CharacterSelectedForceMessage import \
    CharacterSelectedForceMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.character.choice.CharacterSelectedForceReadyMessage import \
    CharacterSelectedForceReadyMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.character.choice.CharacterSelectedSuccessMessage import \
    CharacterSelectedSuccessMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.character.choice.CharacterSelectionMessage import \
    CharacterSelectionMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.character.choice.CharactersListErrorMessage import \
    CharactersListErrorMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.character.choice.CharactersListMessage import \
    CharactersListMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.character.choice.CharactersListRequestMessage import \
    CharactersListRequestMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.character.creation.CharacterCreationRequestMessage import \
    CharacterCreationRequestMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.character.creation.CharacterCreationResultMessage import \
    CharacterCreationResultMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.character.creation.CharacterNameSuggestionRequestMessage import \
    CharacterNameSuggestionRequestMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.character.replay.CharacterReplayRequestMessage import \
    CharacterReplayRequestMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameContextCreateRequestMessage import \
    GameContextCreateRequestMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.initialization.CharacterLoadingCompleteMessage import \
    CharacterLoadingCompleteMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.moderation.PopupWarningClosedMessage import \
    PopupWarningClosedMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.moderation.PopupWarningCloseRequestMessage import \
    PopupWarningCloseRequestMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.startup.StartupActionsListMessage import \
    StartupActionsListMessage
from pydofus2.com.ankamagames.dofus.network.messages.secure.TrustStatusMessage import \
    TrustStatusMessage
from pydofus2.com.ankamagames.dofus.network.messages.subscription.AccountSubscriptionElapsedDurationMessage import \
    AccountSubscriptionElapsedDurationMessage
from pydofus2.com.ankamagames.dofus.network.messages.web.haapi.HaapiApiKeyRequestMessage import \
    HaapiApiKeyRequestMessage
from pydofus2.com.ankamagames.dofus.network.ProtocolConstantsEnum import \
    ProtocolConstantsEnum
from pydofus2.com.ankamagames.jerakine.benchmark.BenchmarkTimer import \
    BenchmarkTimer
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.managers.LangManager import LangManager
from pydofus2.com.ankamagames.jerakine.messages.ConnectionResumedMessage import \
    ConnectionResumedMessage
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.network.messages.ServerConnectionFailedMessage import \
    ServerConnectionFailedMessage
from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage
from pydofus2.com.ankamagames.jerakine.types.DataStoreType import DataStoreType
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority


class GameServerApproachFrame(Frame):
    LOADING_TIMEOUT: int = 60

    def __init__(self):
        self._charactersList = list[BasicCharacterWrapper]()
        self._giftList = []
        self._charaListMinusDeadPeople = []
        self._cssmsg = None
        self._charactersList = list[BasicCharacterWrapper]()
        self._waitingMessages = list[NetworkMessage]()
        self._loadingStart = False
        self._reconnectMsgSend = False
        self._requestedCharacterId = 0
        self.TUTORIAL_SELECTION_IS_AVAILABLE = False
        self.authenticationTicketAccepted = False
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

    def sendAuthTicket(self):
        atmsg = AuthenticationTicketMessage()
        atmsg.init(LangManager().getEntry("config.lang.current"), AuthentificationManager().gameServerTicket)
        ConnectionsHandler().send(atmsg)

    def process(self, msg: Message) -> bool:

        if isinstance(msg, HelloGameMessage):
            self.sendAuthTicket()
            InactivityManager().start()
            KernelEventsManager().send(KernelEvent.AuthenticationTicket)
            return True

        elif isinstance(msg, AuthenticationTicketAcceptedMessage):
            BenchmarkTimer(0.5, self.requestCharactersList).start()
            self.authenticationTicketAccepted = True
            KernelEventsManager().send(KernelEvent.AuthenticationTicketAccepted)
            return True

        elif isinstance(msg, AuthenticationTicketRefusedMessage):
            return True

        elif isinstance(msg, CharactersListMessage):
            import pydofus2.com.ankamagames.dofus.logic.game.common.frames.PlayedCharacterUpdatesFrame as pcuF

            clmsg = msg
            Kernel().worker.addFrame(pcuF.PlayedCharacterUpdatesFrame())
            self._charactersList = clmsg.characters
            server = PlayerManager().server
            if (
                FeatureManager().isFeatureWithKeywordEnabled("server.heroic")
                or server.gameTypeId == GameServerTypeEnum.SERVER_TYPE_EPIC
            ):
                PlayerManager().charactersList.clear()
                for chi in clmsg.characters:
                    if chi.deathMaxLevel > chi.level:
                        bonusXp = 6
                    else:
                        bonusXp = 3
                    o = BasicCharacterWrapper.create(
                        chi.id,
                        chi.name,
                        chi.level,
                        chi.entityLook,
                        chi.breed,
                        chi.sex,
                        chi.deathState,
                        chi.deathCount,
                        chi.deathMaxLevel,
                        bonusXp,
                        False,
                    )
                    PlayerManager().charactersList.append(o)
            else:
                bonusXpFeatureActivated = FeatureManager().isFeatureWithKeywordEnabled(
                    "character.xp.bonusForYoungerCharacters"
                )
                for cbi in clmsg.characters:
                    bonusXp = 1
                    if bonusXpFeatureActivated:
                        for cbi2 in clmsg.characters:
                            if cbi2.id != cbi.id and cbi2.level > cbi.level and bonusXp < 4:
                                bonusXp += 1
                    o = BasicCharacterWrapper.create(
                        cbi.id, cbi.name, cbi.level, cbi.entityLook, cbi.breed, cbi.sex, 0, 0, 0, bonusXp, False
                    )
                    PlayerManager().charactersList.append(o)
            table = PrettyTable()
            table.field_names = [
                "ID",
                "Name",
                "Level",
                "Breed",
                "Sex",
                "Death State",
                "Death Count",
                "Max Death Level",
                "Bonus XP",
            ]
            for character in PlayerManager().charactersList:
                table.add_row(
                    [
                        character.id,
                        character.name,
                        character.level,
                        character.breed.name,
                        character.sex,
                        character.deathState,
                        character.deathCount,
                        character.deathMaxLevel,
                        character.bonusXp,
                    ]
                )
            Logger().info(f"Characters list:\n{table}")
            KernelEventsManager().send(KernelEvent.CharactersList, PlayerManager().charactersList)
            if PlayerManager().allowAutoConnectCharacter:
                characterId = PlayerManager().autoConnectOfASpecificCharacterId
                KernelEventsManager().once(
                    KernelEvent.CharacterSelectedForce,
                    callback=lambda event, charId: None,
                    timeout=1,
                    ontimeout=lambda listener: self.requestCharacterSelect(characterId, False),
                )

            return True

        elif isinstance(msg, ServerConnectionFailedMessage):
            PlayerManager().destroy()
            return True

        elif isinstance(msg, AlreadyConnectedMessage):
            PlayerManager().wasAlreadyConnected = True
            return True

        elif isinstance(msg, CharactersListErrorMessage):
            KernelEventsManager().send(KernelEvent.ClientCrashed, "Characters list error")
            return True

        elif isinstance(msg, AccountCapabilitiesMessage):
            PlayerManager().adminStatus = msg.status
            PlayerManager().canCreateNewCharacter = msg.canCreateNewCharacter
            if msg.tutorialAvailable:
                self.TUTORIAL_SELECTION_IS_AVAILABLE = True
            KernelEventsManager().send(KernelEvent.TutorielAvailable, msg.tutorialAvailable)
            KernelEventsManager().send(KernelEvent.CharacterCreationStart, [["create"]])
            return True

        elif isinstance(msg, CharacterSelectedSuccessMessage):
            cssmsg = msg
            self._loadingStart = time.perf_counter()
            if Kernel().worker.getFrameByName("ServerSelectionFrame"):
                Kernel().worker.removeFrameByName("ServerSelectionFrame")
            PlayedCharacterManager().infos = cssmsg.infos
            DataStoreType.CHARACTER_ID = str(cssmsg.infos.id)
            Kernel().worker.addFrame(WorldFrame())
            Kernel().worker.addFrame(AlignmentFrame())
            Kernel().worker.addFrame(SynchronisationFrame())
            Kernel().worker.addFrame(SpellInventoryManagementFrame())
            Kernel().worker.addFrame(InventoryManagementFrame())
            Kernel().worker.addFrame(ContextChangeFrame())
            Kernel().worker.addFrame(MountFrame())
            Kernel().worker.addFrame(JobsFrame())
            Kernel().worker.addFrame(SocialFrame())
            Kernel().worker.addFrame(QuestFrame())
            Kernel().worker.addFrame(AveragePricesFrame())
            Kernel().worker.addFrame(NpcFrame())
            Kernel().worker.addFrame(PartyFrame())
            KernelEventsManager().send(KernelEvent.CharacterSelectionSuccess, cssmsg.infos)

            # if Kernel().beingInReconection and not self._reconnectMsgSend:
            #     self._reconnectMsgSend = True
            #     ConnectionsHandler().send(CharacterSelectedForceReadyMessage())

            self._cssmsg = cssmsg
            PlayedCharacterManager().infos = self._cssmsg.infos
            DataStoreType.CHARACTER_ID = str(self._cssmsg.infos.id)
            now = time.perf_counter()
            delta = now - self._loadingStart
            if delta > self.LOADING_TIMEOUT:
                Logger().warn(f"Client took too long to load ({delta}s).")
            return True

        elif isinstance(msg, CharacterLoadingCompleteMessage):
            Kernel().worker.removeFrame(self)
            gccrmsg = GameContextCreateRequestMessage()
            ConnectionsHandler().send(gccrmsg)
            return True

        elif isinstance(msg, ConnectionResumedMessage):
            return True

        elif isinstance(msg, CharacterSelectedForceMessage):
            KernelEventsManager().send(KernelEvent.CharacterSelectedForce, msg.id)
            if not self._reconnectMsgSend:
                Kernel().beingInReconection = True
                self.characterId = msg.id
                self._reconnectMsgSend = True
                ConnectionsHandler().send(CharacterSelectedForceReadyMessage())
            return True

        elif isinstance(msg, BasicTimeMessage):
            btmsg = msg
            TimeManager().serverTimeLag = float(
                btmsg.timestamp + btmsg.timezoneOffset * 60 * 1000 - datetime.now().timestamp()
            )
            TimeManager().serverUtcTimeLag = btmsg.timestamp - datetime.now().timestamp()
            TimeManager().timezoneOffset = btmsg.timezoneOffset * 60 * 1000
            TimeManager().dofusTimeYearLag = -1370
            return True

        elif isinstance(msg, AccountSubscriptionElapsedDurationMessage):
            PlayerManager().subscriptionDurationElapsed = msg.subscriptionElapsedDuration
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
                Logger().warn("Empty Gift List Received")
            return True

        elif isinstance(msg, PopupWarningClosedMessage):
            return True

        elif isinstance(msg, PopupWarningCloseRequestAction):
            pwcrmsg = PopupWarningCloseRequestMessage()
            ConnectionsHandler().send(pwcrmsg)
            return True

        elif isinstance(msg, CharacterSelectionAction):
            characterId = msg.characterId
            self.requestCharacterSelect(characterId)
            return True

        elif isinstance(msg, CharacterSelectedErrorMessage):
            KernelEventsManager().send(KernelEvent.CharacterImpossibleSelection, self._requestedCharacterId)
            self._requestedCharacterId = 0
            return True

        elif isinstance(msg, CharacterCreationResultMessage):
            if msg.result == 0:
                self.requestCharactersList()
            return True

        elif isinstance(msg, TrustStatusMessage):
            PlayerManager().isSafe = msg.certified
            if not msg.certified:
                Logger().warn("Client is not certified!")
            return True

        return False

    def pulled(self) -> bool:
        return True

    def pushed(self) -> bool:
        Kernel().worker.addFrame(MiscFrame())
        return True

    def requestCharactersList(self) -> None:
        if ConnectionsHandler().conn:
            clrmsg = CharactersListRequestMessage()
            clrmsg.init()
            ConnectionsHandler().send(clrmsg)
        else:
            KernelEventsManager().send(
                KernelEvent.ClientCrashed, "No connection to server found while requesting characters list"
            )

    def requestNameSuggestion(self):
        msg = CharacterNameSuggestionRequestMessage()
        msg.init()
        ConnectionsHandler().send(msg)

    def requestCharacterCreation(self, name, breedId, sex, colors, cosmeticId):
        if not PlayerManager().canCreateNewCharacter:
            return KernelEventsManager().send(KernelEvent.ClientCrashed, "Cannot create a new character!")
        msg = CharacterCreationRequestMessage()
        if len(colors) > ProtocolConstantsEnum.MAX_PLAYER_COLOR:
            return KernelEventsManager().send(
                KernelEvent.ClientCrashed, f"Too many colors ({len(colors)}) for character creation!"
            )
        while len(colors) < ProtocolConstantsEnum.MAX_PLAYER_COLOR:
            colors.push(-1)
        msg.init(str(name), int(breedId), bool(sex), colors, cosmeticId)
        ConnectionsHandler().send(msg)

    def requestHaapiApiKey(self):
        msg = HaapiApiKeyRequestMessage()
        msg.init()
        ConnectionsHandler().send(msg)

    def requestCharacterSelect(self, characterId, replay=False):
        if self._requestedCharacterId != 0:
            Logger().warn(f"Character {self._requestedCharacterId} is already being selected!")
            return

        selectable_characters_ids = [int(char.id) for char in self._charactersList]
        Logger().debug(f"Selectable characters ids: {selectable_characters_ids}")
        if int(characterId) not in selectable_characters_ids:
            KernelEventsManager().send(
                KernelEvent.ClientCrashed, f"Character {characterId} not found in the characters list!"
            )
            return

        self._requestedCharacterId = characterId
        if self.TUTORIAL_SELECTION_IS_AVAILABLE:
            cfsmsg = CharacterFirstSelectionMessage()
            cfsmsg.init(False, characterId)
            ConnectionsHandler().send(cfsmsg)

        elif replay:
            crrmsg = CharacterReplayRequestMessage()
            crrmsg.init(characterId)
            ConnectionsHandler().send(crrmsg)

        else:
            msg = CharacterSelectionMessage()
            msg.init(characterId)
            ConnectionsHandler().send(msg)
