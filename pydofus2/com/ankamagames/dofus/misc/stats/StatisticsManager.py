import math
from pydofus2.com.ankamagames.berilia.managers.EventsHandler import EventsHandler
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.misc.stats.StatsAction import StatsAction
from pydofus2.com.ankamagames.dofus.misc.utils.HaapiKeyManager import HaapiKeyManager
from pydofus2.com.ankamagames.jerakine.data.XmlConfig import XmlConfig
from pydofus2.com.ankamagames.jerakine.managers.StoreDataManager import StoreDataManager
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton
from pydofus2.com.ankamagames.jerakine.types.DataStoreType import DataStoreType
from pydofus2.com.ankamagames.jerakine.types.enums.DataStoreEnum import DataStoreEnum


class StatisticsManager(EventsHandler, metaclass=Singleton):
    NORMAL_ERROR = "No information received from the server ..."

    def __init__(self):
        self._statsAssoc = {}
        self._stats = {}
        # self._frame = StatisticsFrame(self._stats)  # Replace with actual Python equivalent
        self._componentsStats = {}
        self._firstTimeUserExperience = {}
        self._removedStats = []
        self._actionsSent = []
        self._dataStoreType = None
        self.initDataStoreType()
        # self._dateTimeFormatter = ...  # Set up Python's datetime formatter as needed
        self._exiting = False
        self._stepByStep = None
        self._sentryReported = False
        self._apiCredentials = None  # Define the ApiUserCredentials class in Python

    def initDataStoreType(self):
        if not self._dataStoreType or self._dataStoreType.category != "statistics":
            self._dataStoreType = DataStoreType("statistics", True, DataStoreEnum.LOCATION_LOCAL, DataStoreEnum.BIND_COMPUTER)

    @property
    def sending(self):
        return len(self._actionsSent) > 0

    def onConfigfileLoaded(self):
        self._apiCredentials = ApiUserCredentials("", XmlConfig().getEntry("config.haapiUrlAnkama"), None) 
        self._gameApi = GameApi(self._apiCredentials)
        self.sendPendingEvents()

    def onGameSessionReady(self, event):
        HaapiKeyManager().remove_listener(GameSessionReadyEvent.READY, self.onGameSessionReady)
        self.setGameSessionId(HaapiKeyManager().getGameSessionId())
        sss = SessionStartStats()
        self.sendPendingEvents()

    def onAccountSessionReady(self, event):
        HaapiKeyManager().remove_listener(AccountSessionReadyEvent.READY, self.onAccountSessionReady)
        def callback(apiKey):
            self._apiCredentials.apiToken = apiKey
            self._accountApi = AccountApi(self._apiCredentials)
            self.sendDeviceInfos()
        HaapiKeyManager().callWithApiKey(callback)
    
    @property
    def statsEnabled(self):
        return self._statsAssoc is not None
    
    @statsEnabled.setter
    def statsEnabled(self, value):
        self._statsAssoc = value
        
    def startFirstTimeUserExperience(self, pUserId):
        for uiName in self._statsAssoc:
            if self._statsAssoc[uiName].ftue:
                self._firstTimeUserExperience(uiName, True) 
        StoreDataManager().setData(self._dataStoreType, f"firstTimeUserExperience-{pUserId}", pUserId, self._firstTimeUserExperience)
    
    def setFirstTimeUserExperience(self, pUiName, pValue):
        self._firstTimeUserExperience[pUiName] = pValue

    def startStats(self, pStatsName: str, *args):
        customStatsInfo = self._statsAssoc[pStatsName]
        if customStatsInfo and (not customStatsInfo.ftue or self._firstTimeUserExperience.get(pStatsName)):
            self._stats[pStatsName] = customStatsInfo.statsClass(*args)
            removedIndex = self._removedStats.find(pStatsName)
            if removedIndex != -1:
                self._removedStats.pop(removedIndex)
                del self._stats[pStatsName]
    
    def init(self):
        if not self._pendingActions:
            self._pendingActions = []
            savedStats = StoreDataManager().getData(self._dataStoreType, "statsActions")
            StoreDataManager().setData(self._dataStoreType, "statsActions", None)
            if savedStats:
                for savedStatsAction in savedStats:
                    action = StatsAction.fromString(savedStatsAction)
                    if action:
                        self._pendingActions.append(action)

        self.sendPendingEvents()
        self.registerStats("pseudoChoice", NicknameRegistrationStats)
        self.registerStats("serverListSelection", ServerListSelectionStats, True)
        self.registerStats("characterCreation", CharacterCreationStats, True)
        self.registerStats("cinematic", CinematicStats, True)
        self.registerStats("tutorial", TutorialStats, True)
        self.registerStats("advancedTutorial", AdvancedTutorialStats, True)
        self.registerStats("payZone", PayZoneUiStats)
        self.registerStats("payZoneArrival", PayZoneStats)
        self.registerStats("updateInformation", UpdateInformationStats)
        self.registerStats("configShortcuts", ConfigShortcutStats)
        self.registerStats("shortcuts", ShortcutsStats)
        self.registerStats("auctionBeta", AuctionBetaStats)
        self.registerStats("pvpArena", KolizeumStats)
        self.registerStats("shopNavigation", ShopNavigationStats)
        self.registerStats("userActivity", UserActivitiesStats)
        self.registerStats("openBox", OpenBoxStats)
        self.registerStats("smithMagicAdvanced", SmithMagicAdvancedStats)
        self.registerStats("getArticles", GetArticlesStats)
        self.registerStats("bakNavigation", BakNavigationStats)
        self.registerStats("gameGuide", GameGuideStats)
        self.registerStats("bannerMenu", BannerStats)
        self.registerStats("cartography", CartographyStats)
        self.registerStats("chinq", ChinqStats)
        self.registerStats("suggestions", SuggestionsStats)
        self.registerStats("logBook", LogBookStats)

        Berilia().on(UiRenderEvent.UIRenderComplete, self.onUiLoaded)
        Berilia().on(UiUnloadEvent.UNLOAD_UI_STARTED, self.onUiUnloadStart)
        ModuleLogger.active = True
        ModuleLogger.addCallback(self.log)
        HaapiKeyManager().on(GameSessionReadyEvent.READY, self.onGameSessionReady)
        HaapiKeyManager().on(AccountSessionReadyEvent.READY, self.onAccountSessionReady)

    def destroy(self): 
        StatsAction.reset()
        ModuleLogger.active = false
        ModuleLogger.removeCallback(self.log)
        Kernel().worker.removeFrame(self._frame)
        self._statsAssoc.clear()
        self._stats.clear()
        self._frame = StatisticsFrame(self._stats)
        self._componentsStats.clear()
        self._firstTimeUserExperience.clear()
        self._removedStats.clear()
        Berilia().removeEventListener(UiRenderEvent.UIRenderComplete, self.onUiLoaded)
        Berilia().removeEventListener(UiUnloadEvent.UNLOAD_UI_STARTED, self.onUiUnloadStart)
        HaapiKeyManager().removeEventListener(GameSessionReadyEvent.READY, self.onGameSessionReady)
        HaapiKeyManager().removeEventListener(AccountSessionReadyEvent.READY, self.onAccountSessionReady)
        if not self._exiting:
            SessionEndStats()
            self.init()
        
    @property
    def frame(self):
        return self._frame

    def saveActionTimestamp(self, pActionId, pTimestamp):
        StoreDataManager().setData(self._dataStoreType, self.getActionDataId(pActionId), pTimestamp)

    def getActionTimestamp(self, pActionId):
        data = StoreDataManager().getData(self._dataStoreType, self.getActionDataId(pActionId))
        return data if isinstance(data, float) and not math.isnan(data) else float('nan')

    def deleteTimeStamp(self, pActionId):
        self.saveActionTimestamp(pActionId, float('nan'))

    def sendAction(self, action):
        if action in self._pendingActions:
            return
        self._pendingActions.append(action)
        self.sendPendingEvents()

    def sendActions(self, actions):
        for action in actions:
            if action not in self._pendingActions:
                self._pendingActions.append(action)
        self.sendPendingEvents()

    def setAccountId(self, pAccountId):
        for action in self._pendingActions:
            if action.hasParam("account_id") and action.user == StatsAction.getUserId():
                action.setParam("account_id", pAccountId)

    def setGameSessionId(self, gameSessionId):
        for action in self._pendingActions:
            if action.user == StatsAction.getUserId() and not action.gameSessionId:
                action.gameSessionId = gameSessionId

    def sendActionsAndExit(self):
        self._exiting = True
        SessionEndStats()  # Assuming this initializes or does something necessary
        if self.sendPendingEvents():
            return True
        self.quit()
        return False

    def hasActionsToSend(self):
        if self.sending:
            return True
        return len(self.getEventsToSend()) > 0

    def formatDate(self, pDate):
        return self._dateTimeFormatter.formatUTC(pDate)