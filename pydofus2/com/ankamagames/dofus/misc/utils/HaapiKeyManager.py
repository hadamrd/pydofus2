import threading
from threading import Timer

from pydofus2.com.ankamagames.atouin.Haapi import Haapi
from pydofus2.com.ankamagames.berilia.managers.EventsHandler import \
    EventsHandler
from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import \
    KernelEventsManager
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import \
    ConnectionsHandler
from pydofus2.com.ankamagames.dofus.misc.utils.HaapiEvent import HaapiEvent
from pydofus2.com.ankamagames.dofus.network.messages.web.haapi.HaapiApiKeyRequestMessage import \
    HaapiApiKeyRequestMessage
from pydofus2.com.ankamagames.jerakine.benchmark.BenchmarkTimer import \
    BenchmarkTimer
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton


class HaapiKeyManager(EventsHandler, metaclass=Singleton):
    _instance = None
    ONE_HOUR_IN_S = 3600

    def __init__(self):
        self._apiKey = None
        self._gameSessionId = 0
        self._accountSessionId = None
        self._tokens = {}  # Dictionary equivalent in Python
        self._askedApiKey = threading.Event()
        self._askedToken = False
        self._askedTokens = []  # Vector equivalent in Python
        self._apiKeyExpirationTimer = BenchmarkTimer(self.ONE_HOUR_IN_S, self.onApiKeyExpiration)
        self._apikey_listeners = []
        super().__init__()

    def onApiKeyExpiration(self):
        self._apiKey = None
        self._askedApiKey.clear()

    def getAccountSessionId(self):
        return self._accountSessionId

    def getGameSessionId(self):
        return self._gameSessionId

    def pullToken(self, gameId):
        if gameId not in self._tokens:
            Logger().error("No token available for gameID {}".format(gameId))
            return None
        value = str(self._tokens.pop(gameId))
        return value

    def askToken(self, gameId):
        if gameId in self._askedTokens:
            Logger().debug("Token already asked for gameID {}".format(gameId))
            return
        self._askedTokens.append(gameId)
        self.callWithApiKey(lambda apiKey: self.nextToken())

    def nextToken(self):
        if self._askedToken or len(self._askedTokens) == 0:
            return
        self._askedToken = True
        try:
            gameId = self._askedTokens.pop(0)
            token = Haapi().createToken(gameId, 0, apikey=self._apiKey)
            self._tokens[gameId] = token
            self.send(HaapiEvent.TokenReadyEvent, gameId, token)
            self._askedToken = False
            self.nextToken()
        except Exception as e:
            Logger().debug(f"Account Api Error while creating token for game {gameId}: {e}")
            self._askedToken = False
            self.nextToken()

    def destroy(self):
        HaapiKeyManager._instance = None

    def callWithApiKey(self, callback):
        Logger().debug("CALL WITH API KEY")
        if self._apiKey is not None:
            Logger().debug("CALL WITH API KEY :: API KEY IS NOT NULL")
            callback(self._apiKey)
        else:
            Logger().debug("CALL WITH API KEY :: API KEY IS NULL")
            if not Kernel().gameServerApproachFrame:
                return KernelEventsManager().onceFramePushed("GameServerApproachFrame", lambda: self.callWithApiKey(callback))
            self._apikey_listeners.append(callback)
            if self._askedApiKey.is_set():
                return
            KernelEventsManager().once(KernelEvent.HaapiApiKeyReady, lambda _, haapikey: self.saveApiKey(haapikey), priority=10)
            if not Kernel().gameServerApproachFrame.authenticationTicketAccepted:
                Logger().debug("Cannot call with API key, until authentication ticket is accepted")
                KernelEventsManager().once(KernelEvent.AuthenticationTicketAccepted, self.onAuthTicketAccepted)
            elif not self._askedApiKey.is_set():
                self.onAuthTicketAccepted()
        
    def onAuthTicketAccepted(self, event=None):
        Logger().debug("CALL WITH API KEY :: ASK FOR API KEY")
        self._askedApiKey.set()
        ConnectionsHandler().send(HaapiApiKeyRequestMessage())
             
    def saveApiKey(self, haapiKey):
        Logger().debug("SAVE API KEY")
        self._apiKey = haapiKey
        self._askedApiKey.clear()
        Haapi().account_apikey = haapiKey
        self._apiKeyExpirationTimer = BenchmarkTimer(self.ONE_HOUR_IN_S, self.onApiKeyExpiration)
        self._apiKeyExpirationTimer.start()
        for listener in self._apikey_listeners:
            listener(haapiKey)
        self._apikey_listeners = []

    def saveGameSessionId(self, key):
        self._gameSessionId = int(key)
        Haapi().game_sessionId = int(key)
        self.send(HaapiEvent.GameSessionReadyEvent, self._gameSessionId)

    def saveAccountSessionId(self, key):
        self._accountSessionId = key
        Haapi().account_sessionId = key
        self.send(HaapiEvent.AccountSessionReadyEvent, self._accountSessionId)

    def destroy(self):
        HaapiKeyManager.clear()