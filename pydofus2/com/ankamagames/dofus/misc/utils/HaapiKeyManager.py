from threading import Timer

from pydofus2.com.ankamagames.berilia.managers.EventsHandler import \
    EventsHandler
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.kernel.net.ConnectionsHandler import \
    ConnectionsHandler
from pydofus2.com.ankamagames.dofus.misc.utils.HaapiEvent import HaapiEvent
from pydofus2.com.ankamagames.dofus.network.messages.web.haapi.HaapiApiKeyRequestMessage import \
    HaapiApiKeyRequestMessage
from pydofus2.com.ankamagames.jerakine.data.XmlConfig import XmlConfig
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
        self._askedApiKey = False
        self._askedToken = False
        self._askedTokens = []  # Vector equivalent in Python
        self._accountApi = None  # Assuming AccountApi is implemented
        self._apiKeyCallbacks = []
        self._apiKeyExpirationTimer = Timer(self.ONE_HOUR_IN_S, self.onApiKeyExpiration)
        self._retryTimer = Timer(0.5, self.onTimerEnd)
        super().__init__()

    def onApiKeyExpiration(self):
        self._apiKey = None
        self._askedApiKey = False

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
            return
        self._askedTokens.append(gameId)
        self.callWithApiKey(lambda apiKey: self.nextToken())

    def nextToken(self):
        if self._askedToken or len(self._askedTokens) == 0:
            return
        self._askedToken = True
        self._accountApi = AccountApi()
        try:
            token = self._accountApi.create_token(self._askedTokens[0], 0, None)
            gameId = self._askedTokens.pop(0)
            self._tokens[gameId] = token
            self.send(HaapiEvent.TokenReadyEvent, gameId, token)
            self._askedToken = False
            self.nextToken()
        except Exception as e:
            Logger().debug(f"Account Api Error while creating token : {e}")
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
            if self._apiKeyCallbacks is None:
                self._apiKeyCallbacks = []
            self._apiKeyCallbacks.append(callback)
            # Adapt the following to your application's flow
            if not Kernel().gameServerApproachFrame.authenticationTicketAccepted:
                if self._retryTimer is not None:
                    self._retryTimer.cancel()
                self._retryTimer = Timer(0.5, self.onTimerEnd)
                self._retryTimer.start()
            elif not self._askedApiKey and Kernel().gameServerApproachFrame.authenticationTicketAccepted:
                Logger().debug("CALL WITH API KEY :: ASK FOR API KEY")
                ConnectionsHandler().send(HaapiApiKeyRequestMessage());
                self._askedApiKey = True

    def onTimerEnd(self):
        if not Kernel().gameServerApproachFrame.authenticationTicketAccepted:
            Logger().debug("TIMER RESET, NOT AUTHENTICATED")
            self._retryTimer = Timer(0.5, self.onTimerEnd)
            self._retryTimer.start()
        else:
            Logger().debug("TIMER RESET, AUTHENTICATED")
            self._retryTimer = None
            self.callWithApiKey(lambda apiKey: self.saveApiKey(apiKey))
            Logger().debug("ON TIMER END :: ASK FOR API KEY")
            ConnectionsHandler().send(HaapiApiKeyRequestMessage())
            self._askedApiKey = True
            
    def saveApiKey(self, pHaapiKey):
        Logger().debug("SAVE API KEY")
        self._apiKey = pHaapiKey
        self._askedApiKey = False
        self._accountApi = AccountApi(pHaapiKey)
        self._apiKeyExpirationTimer = Timer(self.ONE_HOUR_IN_S, self.onApiKeyExpiration)
        self._apiKeyExpirationTimer.start()
        if self._apiKeyCallbacks:
            for callback in self._apiKeyCallbacks:
                callback(pHaapiKey)
            self._apiKeyCallbacks = None

    def saveGameSessionId(self, key):
        self._gameSessionId = int(key)
        self.send(HaapiEvent.GameSessionReadyEvent, self._gameSessionId)

    def saveAccountSessionId(self, key):
        self._accountSessionId = key
        self.send(HaapiEvent.AccountSessionReadyEvent, self._accountSessionId)

    def destroy(self):
        HaapiKeyManager.clear()