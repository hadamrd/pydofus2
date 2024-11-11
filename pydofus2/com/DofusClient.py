import atexit
import locale
import sys
import threading
import time
import traceback
from datetime import datetime
from re import T
from time import perf_counter
from typing import TYPE_CHECKING, Type, TypeVar

from pydofus2.com.ankamagames.atouin.Haapi import Haapi
from pydofus2.com.ankamagames.atouin.HaapiEventsManager import HaapiEventsManager
from pydofus2.com.ankamagames.atouin.resources.adapters.ElementsAdapter import ElementsAdapter
from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager
from pydofus2.com.ankamagames.berilia.managers.Listener import Listener
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import ConnectionsHandler
from pydofus2.com.ankamagames.dofus.kernel.net.DisconnectionReasonEnum import DisconnectionReasonEnum
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import PlayerManager
from pydofus2.com.ankamagames.dofus.logic.connection.actions.LoginValidationWithTokenAction import (
    LoginValidationWithTokenAction as LVA_WithToken,
)
from pydofus2.com.ankamagames.dofus.logic.connection.managers.AuthenticationManager import AuthenticationManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.misc.utils.GameID import GameID
from pydofus2.com.ankamagames.dofus.misc.utils.HaapiEvent import HaapiEvent
from pydofus2.com.ankamagames.dofus.misc.utils.HaapiKeyManager import HaapiKeyManager
from pydofus2.com.ankamagames.dofus.network.enums.ChatActivableChannelsEnum import ChatActivableChannelsEnum
from pydofus2.com.ankamagames.dofus.network.enums.ServerStatusEnum import ServerStatusEnum
from pydofus2.com.ankamagames.jerakine.benchmark.BenchmarkTimer import BenchmarkTimer
from pydofus2.com.ankamagames.jerakine.data.ModuleReader import ModuleReader
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.network.messages.TerminateWorkerMessage import TerminateWorkerMessage
from pydofus2.com.ankamagames.jerakine.resources.adapters.AdapterFactory import AdapterFactory
from pydofus2.com.ClientStatusEnum import ClientStatusEnum
from pydofus2.Zaap.ZaapDecoy import ZaapDecoy

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
    from pydofus2.com.ankamagames.jerakine.network.ServerConnection import ServerConnection

# Set the locale to the locale identifier associated with the current language
# The '.UTF-8' suffix specifies the character encoding
locale.setlocale(locale.LC_ALL, Kernel().getLocaleLang() + ".UTF-8")
global_data_lock = threading.Lock()
T = TypeVar("T")


class DofusClient(threading.Thread):
    lastLoginTime = None
    minLoginInterval = 60 * 3
    LOGIN_TIMEOUT = 35
    with global_data_lock:
        _running_clients = list["DofusClient"]()

    def __init__(self, name="DofusClient"):
        super().__init__(name=name)
        self._registeredInitFrames = []
        self._registeredGameStartFrames = []
        self._customEventListeners = []
        self._shutdownListeners = []
        self._statusChangedListeners = []
        self._lock = None
        self._apikey = None
        self._accountId = None
        self._chatToken = None
        self._certId = ""
        self._certHash = ""
        self._serverId = 0
        self._characterId = None
        self._loginToken = None
        self._mule = False
        self._shutdownReason = None
        self._crashed = False
        self._shutdownMessage = ""
        self._reconnectRecord = []
        self._ended_correctly = False
        self._banned = False
        self._taking_nap = False
        self._startTime = None
        self._status = None
        self.kernel = None
        self.terminated = threading.Event()

    def initListeners(self):
        KernelEventsManager().once(
            KernelEvent.CharacterSelectionSuccess,
            self.onCharacterSelectionSuccess,
            originator=self,
        )
        KernelEventsManager().onceMapProcessed(self.onInGame)
        KernelEventsManager().on_multiple(
            [
                (KernelEvent.SelectedServerRefused, self.onServerSelectionRefused),
                (KernelEvent.ClientCrashed, self.crash),
                (KernelEvent.ClientShutdown, self.shutdown),
                (KernelEvent.ClientRestart, self.onRestart),
                (KernelEvent.ClientReconnect, self.onReconnect),
                (KernelEvent.ClientClosed, self.onConnectionClosed),
                (KernelEvent.PlayerLoginSuccess, self.onLoginSuccess),
                (KernelEvent.CharacterImpossibleSelection, self.onCharacterImpossibleSelection),
                (KernelEvent.FightStarted, self.onFight),
                (KernelEvent.HaapiApiKeyReady, self.onHaapiApiKeyReady),
                (KernelEvent.TextInformation, self.onChannelTextInformation),
                (KernelEvent.ClientStatusUpdate, self.onStatusUpdate),
            ],
            originator=self,
        )
        for event_id, callback, kwargs in self._customEventListeners:
            KernelEventsManager().on(event_id, callback, **kwargs, originator=self)

    @property
    def worker(self):
        return Kernel().worker

    def addEventListener(self, event, callback, **kwargs):
        self._customEventListeners.append((event, callback, kwargs))

    def onStatusUpdate(self, event, status: ClientStatusEnum, data=None):
        if data is None:
            data = {}
        self._status = status
        for listener in self._statusChangedListeners:
            BenchmarkTimer(0.1, lambda: listener(self, status, data)).start()

    def init(self):
        Logger().info("Initializing ...")
        ZaapDecoy.SESSIONS_LAUNCH += 1
        atexit.register(self.at_exit)
        self.zaap = ZaapDecoy(self._apikey)
        self.kernel = Kernel()
        self.kernel.init()
        AdapterFactory.addAdapter("ele", ElementsAdapter)
        # AdapterFactory.addAdapter("dlm", MapsAdapter)
        self.kernel.isMule = self._mule
        ModuleReader._clearObjectsCache = True
        self._shutdownReason = None
        self.initListeners()
        Logger().info("Initialized")
        return True

    def setCredentials(self, apikey, certId=0, certHash=""):
        self._apikey = apikey
        self._certId = certId
        self._certHash = certHash

    def setApiKey(self, apiKey):
        self._apikey = apiKey

    def setLoginToken(self, token):
        self._loginToken = token

    def setCertificate(self, certId, certHash):
        self._certId = certId
        self._certHash = certHash

    def setAutoServerSelection(self, serverId, characterId=None):
        self._serverId = serverId
        self._characterId = characterId

    def registerInitFrame(self, frame: "Frame"):
        self._registeredInitFrames.append(frame)

    def registerGameStartFrame(self, frame: "Frame"):
        self._registeredGameStartFrames.append(frame)

    def onChannelTextInformation(self, event, text, channelId, timestamp):
        Logger().info(f"[{timestamp}][{ChatActivableChannelsEnum.to_name(channelId)}] {text}")

    def onCharacterSelectionSuccess(self, event, characterBaseInformations):
        Logger().info("Adding game start frames")
        for frame in self._registeredGameStartFrames:
            self.worker.addFrame(frame)

    def onInGame(self):
        Logger().info("Character entered game server successfully")

    def crash(self, event, message, reason=DisconnectionReasonEnum.EXCEPTION_THROWN):
        KernelEventsManager().send(
            KernelEvent.ClientStatusUpdate, ClientStatusEnum.CRASHED, {"reason": reason, "message": message}
        )
        self._crashed = True
        self._shutdownReason = reason
        self.shutdown(message, reason)

    def onRestart(self, event, message, afterTime=0):
        Logger().debug(f"Restart requested by event {event.name} for reason: {message}")
        self.onReconnect(event, message, afterTime)

    def onLoginTimeout(self, listener: Listener):
        KernelEventsManager().send(KernelEvent.ClientStatusUpdate, ClientStatusEnum.LOGIN_TIMED_OUT)
        self.worker.process(LVA_WithToken.create(self._serverId != 0, self._serverId))
        listener.armTimer()
        self.lastLoginTime = perf_counter()

    def onFight(self, event):
        ...

    def onHaapiApiKeyReady(self, event, apikey):
        pass

    def onServersList(self, event, serversList, serversUsedList, serversTypeAvailableSlots):
        pass

    def onLoginSuccess(self, event, msg):
        ZaapDecoy.CONNECTED_ACCOUNTS += 1
        HaapiKeyManager().on(HaapiEvent.GameSessionReadyEvent, self.onGameSessionReady)
        Haapi().getLoadingScreen(page=1, accountId=PlayerManager().accountId, lang="en", count=20)
        Haapi().getAlmanaxEvent(lang="en")
        HaapiKeyManager().askToken(GameID.CHAT)

    def onGameSessionReady(self, event, gameSessionId):
        Haapi().game_sessionId = gameSessionId
        HaapiEventsManager().sendStartEvent(gameSessionId)
        KernelEventsManager().send(
            KernelEvent.ClientStatusUpdate, ClientStatusEnum.GAME_SESSION_STARTED, {"gameSessionId": gameSessionId}
        )
        Haapi().getCmsFeeds(site="DOFUS", page=0, lang="en", count=20, apikey=self._apikey)
        HaapiKeyManager().callWithApiKey(
            lambda apikey: Haapi().pollInGameGet(count=20, site="DOFUS", lang="en", page=1, apikey=apikey)
        )

    def onCharacterImpossibleSelection(self, event):
        self.shutdown(
            reason=DisconnectionReasonEnum.EXCEPTION_THROWN,
            message=f"Character {self._characterId} impossible to select in server {self._serverId}!",
        )

    def onServerSelectionRefused(self, event, serverId, err_type, server_status, error_text, selectableServers):
        Logger().error(
            f"Server selection refused for reason: {error_text}, error_type: {err_type}, server_status: {server_status}"
        )
        if server_status == ServerStatusEnum.SAVING.value:
            return
        elif server_status == ServerStatusEnum.STOPPING.value:
            self.onReconnect(event, "Server is stopping, will disconnect and retry after 3 minutes...", 3 * 60)
            return
        elif server_status == ServerStatusEnum.OFFLINE.value:
            self.onReconnect(event, "Server is offline, will disconnect and retry after 3 minutes...", 3 * 60)
            return
        elif server_status == ServerStatusEnum.STARTING.value:
            self.onReconnect(event, "Server is starting, will disconnect and retry after 1 minutes...", 1 * 60)
            return
        elif server_status == ServerStatusEnum.NOJOIN.value:
            if error_text != "SubscribersOnly":
                self.onReconnect(event, "Server is not joinable, will disconnect and retry after 3 minutes...", 3 * 60)
                return
            else:
                error_text = "You can't join the server because its subscriber only and you are not subscribed!"
        self._crashed = True
        self.shutdown(reason=DisconnectionReasonEnum.EXCEPTION_THROWN, message=error_text)

    def onConnectionClosed(self, event, connId):
        KernelEventsManager().send(
            KernelEvent.ClientStatusUpdate, ClientStatusEnum.CONNECTION_CLOSED, {"connId": connId}
        )

    def at_exit(self):
        if not self._ended_correctly:
            Logger().error("Client not ended correctly, sending end event")
            if Haapi().game_sessionId:
                HaapiEventsManager().sendEndEvent()
                ZaapDecoy.CONNECTED_ACCOUNTS.remove(PlayerManager().accountId)
                self.kernel.reset()
                Logger().info("goodby crual world")
                self.terminated.set()
                for callback in self._shutdownListeners:
                    Logger().info(f"Calling shutdown callback {callback}")
                    callback(self.name, self._shutdownMessage, self._shutdownReason)
            else:
                Logger().info("Haapi game session not ready, not sending end event")
            self._ended_correctly = True
            self._running_clients.remove(self)

    def prepareLogin(self):
        PlayedCharacterManager().instanceId = self.name
        if self._characterId:
            PlayerManager().allowAutoConnectCharacter = True
            PlayedCharacterManager().id = int(self._characterId)
            PlayerManager().autoConnectOfASpecificCharacterId = int(self._characterId)
            Logger().info(f"Auto connect character id set to {self._characterId} for server {self._serverId}")
        Logger().info("Adding game start frames ...")
        for frame in self._registeredInitFrames:
            self.worker.addFrame(frame)
        if not self._loginToken:
            if self._apikey is None:
                return self.shutdown(
                    message="Unable to login for reason : No apikey and certificate or login token provided!",
                    reason=DisconnectionReasonEnum.EXCEPTION_THROWN,
                )
            try:
                self._loginToken = self.zaap.getLoginToken(GameID.DOFUS, self._certId, self._certHash, self._apikey)
            except Exception as exc:
                return self.shutdown(
                    message=f"Generate login failed with error: {exc}",
                    reason=DisconnectionReasonEnum.EXCEPTION_THROWN,
                )
        AuthenticationManager().setToken(self._loginToken)
        self.waitNextLogin()
        self._loginToken = None

    def onReconnect(self, event, message, afterTime=0):
        Logger().warning(f"Reconnect requested for reason: {message}")
        now = datetime.now()
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
        self._reconnectRecord.append({"restartTime": formatted_time, "reason": message})
        Kernel().reset(reloadData=True)
        if afterTime:
            Logger().info(f"Taking a nap for {afterTime}sec before reconnecting again")
            KernelEventsManager().send(KernelEvent.ClientStatusUpdate, ClientStatusEnum.TAKING_NAP)
            self._taking_nap = True
            BenchmarkTimer(afterTime, self.initListenersAndLogin).start()
        else:
            self.initListenersAndLogin()

    def initListenersAndLogin(self):
        self._taking_nap = False
        self.initListeners()
        self.prepareLogin()
        self.worker.process(LVA_WithToken.create(self._serverId != 0, self._serverId))

    def waitNextLogin(self):
        if DofusClient.lastLoginTime is not None:
            diff = DofusClient.minLoginInterval - (perf_counter() - DofusClient.lastLoginTime)
            if diff > 0:
                Logger().info(f"ave to wait {diff}sec before reconnecting again")
                self.terminated.wait(diff)
        self.lastLoginTime = perf_counter()

    def shutdown(self, message="", reason=None):
        self._shutdownReason = reason if reason else DisconnectionReasonEnum.WANTED_SHUTDOWN
        self._shutdownMessage = message if message else "Wanted shutdown for unknwon reason"
        if self.kernel:
            Logger().info(f"Shutting down client {self.name} for reason : {self._shutdownReason}")
            KernelEventsManager().send(
                KernelEvent.ClientStatusUpdate, ClientStatusEnum.STOPPING, {"reason": str(self._shutdownReason)}
            )
            self.kernel.worker.process(TerminateWorkerMessage())
        else:
            Logger().warning("Kernel is not running, kernel running instances : " + str(Kernel.__instances))
        return

    def addShutdownListener(self, callback):
        self._shutdownListeners.append(callback)

    @property
    def connection(self) -> "ServerConnection":
        return ConnectionsHandler().conn

    @property
    def registeredInitFrames(self) -> list:
        return self._registeredInitFrames

    @property
    def registeredGameStartFrames(self) -> list:
        return self._registeredGameStartFrames

    @classmethod
    def get_client(cls: Type[T], name) -> T:
        for client in cls._running_clients:
            if client.name == str(name):
                return client
        return None

    @classmethod
    def get_clients(cls: Type[T]) -> list[T]:
        return cls._running_clients

    def run(self):
        try:
            self._startTime = time.time()
            with global_data_lock:
                self._running_clients.append(self)
            self.init()
            self.prepareLogin()
            self.worker.process(LVA_WithToken.create(self._serverId != 0, self._serverId))
            self.worker.run()
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
            self._shutdownMessage = error_trace
            self._crashed = True
            self._shutdownReason = DisconnectionReasonEnum.EXCEPTION_THROWN

        if self._shutdownReason != DisconnectionReasonEnum.WANTED_SHUTDOWN:
            self._crashed = True
            Logger().error(f"Crashed for reason : {self._shutdownReason} :\n{self._shutdownMessage}")

        if self._shutdownReason == DisconnectionReasonEnum.BANNED:
            self._banned = True

        if Haapi().game_sessionId:
            Logger().info("Sending end events")
            try:
                HaapiEventsManager().sendEndEvent()
            except Exception as e:
                Logger().error("Failed to send end events", exc_info=True)

        ZaapDecoy.CONNECTED_ACCOUNTS -= 1

        Kernel().reset()
        Logger().info("goodby cruel world")
        self.terminated.set()
        for callback in self._shutdownListeners:
            Logger().info(f"Calling shutdown listener: {callback.__name__}")
            callback(self._shutdownReason, self._shutdownMessage)
        self._ended_correctly = True
        with global_data_lock:
            self._running_clients.remove(self)
