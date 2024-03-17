import atexit
import json
import locale
import os
import sys
import threading
import traceback
from datetime import datetime
from time import perf_counter, sleep
from typing import TYPE_CHECKING

from ankalauncher.pythonversion.Device import Device

from pydofus2.com.ankamagames.atouin.Haapi import Haapi
from pydofus2.com.ankamagames.atouin.HaapiEventsManager import \
    HaapiEventsManager
from pydofus2.com.ankamagames.atouin.resources.adapters.ElementsAdapter import \
    ElementsAdapter
from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import \
    KernelEventsManager
from pydofus2.com.ankamagames.berilia.managers.Listener import Listener
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import \
    ConnectionsHandler
from pydofus2.com.ankamagames.dofus.kernel.net.DisconnectionReasonEnum import \
    DisconnectionReasonEnum
from pydofus2.com.ankamagames.dofus.logic.common.frames.QueueFrame import \
    QueueFrame
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import \
    PlayerManager
from pydofus2.com.ankamagames.dofus.logic.connection.actions.LoginValidationWithTokenAction import \
    LoginValidationWithTokenAction as LVA_WithToken
from pydofus2.com.ankamagames.dofus.logic.connection.frames.AuthentificationFrame import \
    AuthentificationFrame
from pydofus2.com.ankamagames.dofus.logic.connection.managers.AuthentificationManager import \
    AuthentificationManager
from pydofus2.com.ankamagames.dofus.logic.game.approach.frames.GameServerApproachFrame import \
    GameServerApproachFrame
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import \
    PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.misc.utils.GameID import GameID
from pydofus2.com.ankamagames.dofus.network.enums.ServerStatusEnum import \
    ServerStatusEnum
from pydofus2.com.ankamagames.jerakine.data.ModuleReader import ModuleReader
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.network.messages.TerminateWorkerMessage import \
    TerminateWorkerMessage
from pydofus2.com.ankamagames.jerakine.resources.adapters.AdapterFactory import \
    AdapterFactory

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.jerakine.network.ServerConnection import \
        ServerConnection

# Set the locale to the locale identifier associated with the current language
# The '.UTF-8' suffix specifies the character encoding
locale.setlocale(locale.LC_ALL, Kernel().getLocaleLang() + ".UTF-8")


class DofusClient(threading.Thread):
    APIKEY_NOT_FOUND = 36363
    UNEXPECTED_CLIENT_ERROR = 36364
    lastLoginTime = None
    minLoginInterval = 60 * 3
    LOGIN_TIMEOUT = 35
    MAX_CONN_TRIES = 3

    def __init__(self, name="unknown"):
        super().__init__(name=name)
        self._killSig = threading.Event()
        self._registredInitFrames = []
        self._registredGameStartFrames = []
        self._lock = None
        self._apiKey = None
        self._chatApiKey = None
        self._chatLoginToken = None
        self._certId = ""
        self._certHash = ""
        self._serverId = 0
        self._characterId = None
        self._loginToken = None
        self._conxTries = 0
        self._connectionUnexpectedFailureTimes = []
        self._mule = False
        self._shutDownReason = None
        self._crashed = False
        self._shutDownMessage = ""
        self._reconnectRecord = []
        self._shutDownListeners = []
        self._sessionId = None
        self._haapi: Haapi = None
        self.terminated = threading.Event()
        self._end_events_sent = False

    def send_exit_events(self, apikey, session_id):
        # TODO: send events and shortcuts_list
        print("sending exit events")
        if self._end_events_sent is False:
            Haapi().api_key = apikey
            HaapiEventsManager().sendEndEvents()
            Haapi().endSessionWithApiKey(session_id)

    @property
    def worker(self):
        return Kernel().worker

    def init(self):
        Logger().info("Initializing ...")
        self._haapi = Haapi()
        self._haapi.api_key = self._apiKey
        if not self._sessionId:
            acc = self._haapi.signOnWithApikey(GameID.ZAAP)
            self._haapi.listWithApiKey()
            self._haapi.getAccountStatus()
            self._sessionId = self._haapi.startSessionWithApiKey(acc["id"])
            atexit.register(self.send_exit_events, self._apiKey, self._sessionId)
            Logger().info(f"Session started with id {self._sessionId}")
            self._haapi.getFromCms(template_key="NEWS", site="LAUNCHEREVENTS", lang="en", page=1, count=1)
            self._haapi.getFromCms(template_key="BLOG", site="LAUNCHEREVENTS", lang="en", page=1, count=1)
            self._haapi.getLegalsTou(game=GameID.DOFUS, lang="en", knowVersion=11)
            self._haapi.sendDeviceInfos(
                session_id=acc["id"],
                connection_type="ANKAMA",
                client_type="STANDALONE",
                os="WINDOWS",
                device="PC",
                partner="",
                device_uid=self.get_zaap_deviceuuid(),
            )
            self._haapi.getCmsById(site="LAUNCHEREVENTS", lang="en", id=1687826)
            self._haapi.getFromCms(template_key="CHANGELOG", site="LAUNCHER", lang="en", page=1, count=20)
            self._chatApiKey = self._haapi.getLoginToken(game_id=GameID.CHAT)
            self._haapi.getCarouselForLauncher(site="DOFUS", lang="en", page=1, count=1)
            self._haapi.getFromCms(template_key="NEWS", site="ZAAP_PAGE_DOFUS", lang="en", page=1, count=15)
            self._haapi.getFromCms(template_key="BLOG", site="ZAAP_PAGE_DOFUS", lang="en", page=1, count=15)
            self._haapi.getFromCms(template_key="NEWS", site="LAUNCHER", lang="en", page=1, count=15)
            self._haapi.getFromCms(template_key="BLOG", site="LAUNCHER", lang="en", page=1, count=15)
            self._haapi.getFromCms(template_key="NEWS", site="ZAAP_PAGE_DOFUS", lang="en", page=1, count=3)
            self._haapi.getFromCms(template_key="BLOG", site="ZAAP_PAGE_DOFUS", lang="en", page=1, count=3)
        Kernel().init()
        AdapterFactory.addAdapter("ele", ElementsAdapter)
        # AdapterFactory.addAdapter("dlm", MapsAdapter)
        Kernel().isMule = self._mule
        ModuleReader._clearObjectsCache = True
        self._shutDownReason = None
        self.initListeners()
        Logger().info("Initialized")

    def get_zaap_deviceuuid(self):
        appdata_path = os.getenv("APPDATA")
        settings_file_path = os.path.join(appdata_path, "zaap", "Settings")
        with open(settings_file_path, "r") as file:
            settings_data = json.load(file)
            return settings_data.get("DEVICE_UID")

    @property
    def sessionId(self):
        return self._sessionId

    @sessionId.setter
    def sessionId(self, sessionId):
        self._sessionId = sessionId

    def setApiKey(self, apiKey):
        self._apiKey = apiKey

    def setLoginToken(self, token):
        self._loginToken = token

    def setAutoServerSelection(self, serverId):
        self._serverId = serverId

    def registerInitFrame(self, frame):
        self._registredInitFrames.append(frame)

    def registerGameStartFrame(self, frame):
        self._registredGameStartFrames.append(frame)

    def onCharacterSelectionSuccess(self, event, return_value):
        Logger().info("Adding game start frames")
        for frame in self._registredGameStartFrames:
            self.worker.addFrame(frame())

    def onInGame(self):
        Logger().info("Character entered game server successfully")

    def crash(self, event, message, reason=DisconnectionReasonEnum.EXCEPTION_THROWN):
        self._crashed = True
        self._shutDownReason = reason
        self.shutdown(message, reason)

    def onRestart(self, event, message):
        Logger().debug(f"Restart requested by event {event} for reason: {message}")
        self.onReconnect(event, message)

    def onLoginTimeout(self, listener: Listener):
        self.worker.process(LVA_WithToken.create(self._serverId != 0, self._serverId))
        listener.armTimer()
        self.lastLoginTime = perf_counter()

    def initListeners(self):
        KernelEventsManager().on(KernelEvent.SelectedServerRefused, self.onServerSelectionRefused, originator=self)
        KernelEventsManager().once(
            KernelEvent.CharacterSelectedSuccessfully,
            self.onCharacterSelectionSuccess,
            originator=self,
        )
        KernelEventsManager().onceMapProcessed(
            self.onInGame,
            timeout=self.LOGIN_TIMEOUT,
            ontimeout=self.onLoginTimeout,
            originator=self,
        )
        KernelEventsManager().on(KernelEvent.ClientCrashed, self.crash, originator=self)
        KernelEventsManager().on(KernelEvent.ClientShutdown, self.shutdown, originator=self)
        KernelEventsManager().on(KernelEvent.ClientRestart, self.onRestart, originator=self)
        KernelEventsManager().on(KernelEvent.ClientReconnect, self.onReconnect, originator=self)
        KernelEventsManager().on(KernelEvent.ClientClosed, self.onConnectionClosed, originator=self)
        KernelEventsManager().on(KernelEvent.PlayerLoggedIn, self.onloginSuccess, originator=self)
        KernelEventsManager().on(
            KernelEvent.CharacterImpossibleSelection, self.onCharacterImpossibleSelection, originator=self
        )
        KernelEventsManager().on(KernelEvent.FightStarted, self.onFight)

    def onFight(self, event):
        pass
    
    def onloginSuccess(self, event, ismsg):
        HaapiEventsManager().sendStartEvent()
        self._haapi.getLoadingScreen(page=1, accountId=PlayerManager().accountId, lang="en", count=20)
        self._haapi.getAlmanaxEvent(lang="en")
        self._haapi.getCmsFeeds(site="DOFUS", lang="en", page=0, count=20)
        self._chatLoginToken = self._haapi.getLoginToken(GameID.CHAT, 0, from_dofus=True, api_key=self._chatApiKey)

    def onCharacterImpossibleSelection(self, event):
        self.shutdown(
            DisconnectionReasonEnum.EXCEPTION_THROWN,
            f"Character {self._characterId} impossible to select in server {self._serverId}!",
        )

    def onServerSelectionRefused(self, event, serverId, err_type, server_status, error_text, selectableServers):            
        self._shutDownReason = f"Server selection refused for reason : {error_text}"
        self._crashed = True
        self.shutdown(DisconnectionReasonEnum.EXCEPTION_THROWN, error_text)

    def onConnectionClosed(self, event, connId):
        reason = ConnectionsHandler().handleDisconnection()
        Logger().info(f"Connection '{connId}' closed for reason : {reason}")
        if ConnectionsHandler().hasReceivedMsg:
            if (
                not reason.expected
                and not ConnectionsHandler().hasReceivedNetworkMsg
                and self._conxTries < self.MAX_CONN_TRIES
            ):
                Logger().error(
                    f"The connection was closed unexpectedly. Reconnection attempt {self._conxTries}/{self.MAX_CONN_TRIES}."
                )
                self._conxTries += 1
                self._connectionUnexpectedFailureTimes.append(perf_counter())
                self.onReconnect(None, reason.message)
            else:
                if not reason.expected:
                    self._connectionUnexpectedFailureTimes.append(perf_counter())
                    self.onReconnect(None, "The connection was closed unexpectedly.")
                else:
                    if reason.type == DisconnectionReasonEnum.EXCEPTION_THROWN:
                        self.crash(None, reason.message, reason.type)
                    elif reason.type == DisconnectionReasonEnum.WANTED_SHUTDOWN:
                        self.shutdown(reason.type, reason.message)
                    elif reason.type in [
                        DisconnectionReasonEnum.RESTARTING,
                        DisconnectionReasonEnum.DISCONNECTED_BY_POPUP,
                        DisconnectionReasonEnum.CONNECTION_LOST,
                    ]:
                        self.onRestart(event, reason.message)
                    elif reason.type == DisconnectionReasonEnum.SWITCHING_TO_GAME_SERVER:
                        Kernel().worker.addFrame(GameServerApproachFrame())
                        ConnectionsHandler().connectToGameServer(
                            Kernel().serverSelectionFrame._selectedServer.address,
                            Kernel().serverSelectionFrame._selectedServer.ports[0],
                        )
                    elif reason.type == DisconnectionReasonEnum.CHANGING_SERVER:
                        lva = AuthentificationManager()._lva
                        targetServerId = lva.serverId if lva else None
                        if targetServerId is None:
                            Logger().error(
                                f"Closed connection to change server but no serverId is specified in Auth Manager"
                            )
                        else:
                            Logger().info(f"Switching to target server {targetServerId} server ...")
                            Kernel().worker.addFrame(AuthentificationFrame())
                            Kernel().worker.addFrame(QueueFrame())
                            lva = LVA_WithToken.create(targetServerId != 0, targetServerId)
                            Kernel().worker.process(lva)
                    elif reason.type == DisconnectionReasonEnum.SWITCHING_TO_HUMAN_VENDOR:
                        pass

                    elif reason.type == DisconnectionReasonEnum.DISCONNECTED_BY_USER:
                        pass
        else:
            Logger().warning("The connection hasn't even start or already closed.")

    def prepareLogin(self):
        PlayedCharacterManager().instanceId = self.name
        if self._characterId:
            PlayerManager().allowAutoConnectCharacter = True
            PlayedCharacterManager().id = int(self._characterId)
            PlayerManager().autoConnectOfASpecificCharacterId = int(self._characterId)
        Logger().info("Adding game start frames")
        for frame in self._registredInitFrames:
            self.worker.addFrame(frame())
        if not self._loginToken:
            if self._apiKey is None:
                return self.shutdown(
                    DisconnectionReasonEnum.EXCEPTION_THROWN,
                    msg="Unable to login for reason : No apikey and certificate or login token provided!",
                )
            self._loginToken = self._haapi.getLoginToken(GameID.DOFUS, self._certId, self._certHash)
            if self._loginToken is None:
                return self.shutdown(
                    DisconnectionReasonEnum.EXCEPTION_THROWN,
                    msg="Unable to login for reason : Unable to generate login token!",
                )
        AuthentificationManager().setToken(self._loginToken)
        self.waitNextLogin()
        self._loginToken = None

    def onReconnect(self, event, message, afterTime=0):
        Logger().warning(f"Reconnect requested for reason: {message}")
        now = datetime.now()
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
        self._reconnectRecord.append({"restartTime": formatted_time, "reason": message})
        Kernel().reset(reloadData=True)
        if afterTime:
            self.terminated.wait(afterTime)
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

    def shutdown(self, msg="", reason=None):
        self._shutDownReason = reason if reason else DisconnectionReasonEnum.WANTED_SHUTDOWN
        self._shutDownMessage = msg if msg else "Wanted shutdown"
        if Kernel.getInstance(self.name):
            Logger().info(f"Shutting down client {self.name} for reason : {self._shutDownReason}")
            Kernel.getInstance(self.name).worker.process(TerminateWorkerMessage())
        else:
            Logger().warning("Kernel is not running, kernel running instances : " + str(Kernel._instances))
        return

    def addShutDownListener(self, callback):
        self._shutDownListeners.append(callback)

    @property
    def connection(self) -> "ServerConnection":
        return ConnectionsHandler().conn

    @property
    def registeredInitFrames(self) -> list:
        return self._registredInitFrames

    @property
    def registeredGameStartFrames(self) -> list:
        return self._registredGameStartFrames

    def run(self):
        try:
            self.init()
            self.prepareLogin()
            self.worker.process(LVA_WithToken.create(self._serverId != 0, self._serverId))
            self.worker.run()
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback_in_var = traceback.format_tb(exc_traceback)
            # Start with the current exception's traceback
            error_trace = "\n".join(traceback_in_var) + "\n" + str(exc_value)
            # Check for and add traceback from the cause, if any
            cause = e.__cause__
            while cause:
                cause_traceback = traceback.format_tb(cause.__traceback__)
                error_trace += "\n\n-- Chained Exception --\n"
                error_trace += "\n".join(cause_traceback) + "\n" + str(cause)
                cause = cause.__cause__
            self._shutDownMessage = error_trace
            self._crashed = True
            self._shutDownReason = DisconnectionReasonEnum.EXCEPTION_THROWN

        if self._shutDownReason:
            Logger().info(f"Wanted shutdown for reason : {self._shutDownReason}")
            if self._shutDownMessage:
                Logger().error(f"Crashed for reason : {self._shutDownReason} :\n{self._shutDownMessage}")
        if self._sessionId:
            HaapiEventsManager().sendEndEvent()
            HaapiEventsManager().sendEndEvents()
            Haapi().endSessionWithApiKey(self._sessionId)
            self._end_events_sent = True
        Kernel().reset()
        Logger().info("goodby crual world")
        self.terminated.set()
        for callback in self._shutDownListeners:
            Logger().info(f"Calling shutdown callback {callback}")
            callback(self.name, self._shutDownMessage, self._shutDownReason)
