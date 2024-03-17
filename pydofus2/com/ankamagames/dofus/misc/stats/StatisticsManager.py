import datetime
import math
import platform

from pydofus2.com.ankamagames.berilia.managers.EventsHandler import \
    EventsHandler
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import \
    PlayerManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import \
    PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.misc.DeviceUtils import DeviceUtils
from pydofus2.com.ankamagames.dofus.misc.openApi.ApiUserCredentials import \
    ApiUserCredentials
from pydofus2.com.ankamagames.dofus.misc.stats.custom.SessionEndStats import \
    SessionEndStats
from pydofus2.com.ankamagames.dofus.misc.stats.custom.SessionStartStats import \
    SessionStartStats
from pydofus2.com.ankamagames.dofus.misc.stats.IHookStats import IHookStats
from pydofus2.com.ankamagames.dofus.misc.stats.StatisticsEvent import \
    StatisticsEvent
from pydofus2.com.ankamagames.dofus.misc.stats.StatsAction import StatsAction
from pydofus2.com.ankamagames.dofus.misc.utils.GameID import GameID
from pydofus2.com.ankamagames.dofus.misc.utils.HaapiEvent import HaapiEvent
from pydofus2.com.ankamagames.dofus.misc.utils.HaapiKeyManager import \
    HaapiKeyManager
from pydofus2.com.ankamagames.haapi.client.GameApi import GameApi
from pydofus2.com.ankamagames.jerakine.data.XmlConfig import XmlConfig
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.managers.StoreDataManager import \
    StoreDataManager
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton
from pydofus2.com.ankamagames.jerakine.types.DataStoreType import DataStoreType
from pydofus2.com.ankamagames.jerakine.types.enums.DataStoreEnum import \
    DataStoreEnum


class StatisticsManager(EventsHandler, metaclass=Singleton):
    NORMAL_ERROR = "No information received from the server ..."

    def __init__(self):
        self._statsAssoc = {}
        self._stats = {}
        # self._frame = StatisticsFrame(self._stats)  # Replace with actual Python equivalent
        self._componentsStats = {}
        self._firstTimeUserExperience = {}
        self._removedStats = []
        self._actionsSent = list[StatsAction]()
        self._dataStoreType = None
        self.initDataStoreType()
        self._dateTimeFormatter = "%Y-%m-%dT%H:%M:%S+00:00"
        self._exiting = False
        self._stepByStep = None
        self._sentryReported = False
        self._apiCredentials = None
        self._pendingActions = list[StatsAction]()
        self._gameApi = GameApi()

    def initDataStoreType(self):
        if not self._dataStoreType or self._dataStoreType.category != "statistics":
            self._dataStoreType = DataStoreType(
                "statistics", True, DataStoreEnum.LOCATION_LOCAL, DataStoreEnum.BIND_COMPUTER
            )

    @property
    def sending(self):
        return len(self._actionsSent) > 0

    def onConfigfileLoaded(self):
        self.sendPendingEvents()

    def onGameSessionReady(self, event, gameSessionId):
        self.setGameSessionId(HaapiKeyManager().getGameSessionId())
        SessionStartStats()
        self.sendPendingEvents()

    def onAccountSessionReady(self, event):
        
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
        StoreDataManager().setData(
            self._dataStoreType, f"firstTimeUserExperience-{pUserId}", pUserId, self._firstTimeUserExperience
        )

    def setFirstTimeUserExperience(self, pUiName, pValue):
        self._firstTimeUserExperience[pUiName] = pValue

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
        HaapiKeyManager().once(HaapiEvent.GameSessionReadyEvent, self.onGameSessionReady,  originator=self)
        HaapiKeyManager().once(HaapiEvent.AccountSessionReadyEvent, self.onAccountSessionReady, originator=self)

    def destroy(self):
        StatsAction.reset()
        ModuleLogger.active = False
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
        HaapiKeyManager().remove_listener(GameSessionReadyEvent.READY, self.onGameSessionReady)
        HaapiKeyManager().removeEventListener(AccountSessionReadyEvent.READY, self.onAccountSessionReady)
        if not self._exiting:
            SessionEndStats()
            self.init()

    @property
    def frame(self):
        return self._frame

    def saveActionTimestamp(self, pActionId: int, pTimestamp: int):
        StoreDataManager().setData(self._dataStoreType, self.getActionDataId(pActionId), pTimestamp)

    def getActionTimestamp(self, pActionId):
        data = StoreDataManager().getData(self._dataStoreType, self.getActionDataId(pActionId))
        return data if isinstance(data, float) and not math.isnan(data) else float("nan")

    def deleteTimeStamp(self, pActionId):
        self.saveActionTimestamp(pActionId, float("nan"))

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

    def formatDate(date_obj: datetime.datetime):
        """
        Format a datetime object to a string in the format "yyyy-MM-dd'T'HH:mm:ss+00:00".

        :param date_obj: The datetime object to format.
        :return: A string representing the formatted date.
        """
        formatted_date = date_obj.strftime("%Y-%m-%dT%H:%M:%S+00:00")
        return formatted_date

    def quit(self):
        self.send(StatisticsEvent.ALL_DATA_SENT)
        self.destroy()

    def startStats(self, pStatsName: str, *args):
        customStatsInfo = self._statsAssoc[pStatsName]
        if customStatsInfo and (not customStatsInfo.get('ftue') or self._firstTimeUserExperience.get(pStatsName)):
            self._stats[pStatsName] = customStatsInfo.statsClass(*args)
            if pStatsName in self._removedStats:
                self._removedStats.remove(pStatsName)
                del self._stats[pStatsName]

    def getActionDataId(self, pActionId):
        id = None
        characterName = PlayedCharacterManager().name
        accountName = PlayerManager().nickname
        if characterName:
            id = characterName
        elif accountName:
            id = accountName
        actionId = str(pActionId)
        return f"{id}#{actionId}" if id else str(actionId)

    def log(self, *args):
        if isinstance(args[0], Message):
            for stats in self._stats.values():
                stats.process(args[0], args)
            for componentStats in self._componentsStats:
                if args[1] == componentStats.component:
                    componentStats.process(args[0], args)
        elif len(args) > 1 and args[1] == "hook":
            for stats in self._stats:
                if isinstance(stats, IHookStats):
                    stats.onHook(args[0], args[2])
            for componentStats in self._componentsStats:
                if isinstance(componentStats, IHookStats):
                    componentStats.onHook(args[0], args[2])

    def  registerStats(self, pUiName, pUiStatsClass, pFtue=False):
        self._statsAssoc[pUiName] = {"statClass": pUiStatsClass, "ftue": pFtue}

    def initDataStoreType(self):
        if not self._dataStoreType or self._dataStoreType.category != "statistics":
            self._dataStoreType = DataStoreType(
                "statistics", True, DataStoreEnum.LOCATION_LOCAL, DataStoreEnum.BIND_COMPUTER
            )        

    def sendDeviceInfos(self):
        Logger().info("Calling method SendDeviceInfos")
        try:
            self._accountApi.send_device_infos(
                0,
                AccountApi.sendDeviceInfos_ConnectionTypeEnum_ANKAMA,
                AccountApi.sendDeviceInfos_ClientTypeEnum_STANDALONE,
                platform.system().replace(" ", "").upper(),
                AccountApi.sendDeviceInfos_DeviceEnum_PC,
                None,
                DeviceUtils.deviceUniqueIdentifier(),
                HaapiKeyManager().getAccountSessionId()
            )
        except Exception as e:
            Logger().error("Error while calling Account Api : " + str(e))
        Logger().info("Device info sent successfully")

    def getEventsToSend(self):
        result = []
        gameSessionId = 0
        currentGameSessionId = HaapiKeyManager().getGameSessionId()
        for action in self._pendingActions:
            if not self._exiting and (
                currentGameSessionId != 0
                and (action.gameSessionId == currentGameSessionId and not action.sendOnExit)
                or action.gameSessionId
            ):
                if gameSessionId == 0:
                    gameSessionId = action.gameSessionId
                elif gameSessionId != action.gameSessionId:
                    break
                result.append(action)
                if self._stepByStep == gameSessionId:
                    break
        return result

    def sendPendingEvents(self):
        Logger().info(f"Status: Sending = {len(self._actionsSent)} / Total not sent = {len(self._pendingActions)}")
        if self.sending or not (self._apiCredentials and self._apiCredentials.apiPath):
            return True

        self._actionsSent = self.getEventsToSend()
        
        if self._actionsSent:
            if len(self._actionsSent) == 1:
                action = self._actionsSent[0]
                Logger().info("Calling method SendEvent")

                self._gameApi.send_event(
                    GameID.current,
                    action.gameSessionId,
                    action.id,
                    action.paramsString,
                    action.date,
                    onSuccess=self.onApiCallResult,
                    onError=self.onApiCallError,
                )
            else:
                Logger().info(f"Calling method SendEvents containing {len(self._actionsSent)} events")
                self._gameApi.send_events(
                    GameID.current,
                    self._actionsSent[0].gameSessionId,
                    self.sentEventsToString(),
                    onSuccess=self.onApiCallResult,
                    onError=self.onApiCallError,
                )
            return True
        return False

    def sentEventsToString(self):
        eventString = "["
        for i, action in enumerate(self._actionsSent):
            eventString += action.toString()
            if i < len(self._actionsSent) - 1:
                eventString += ","
        return eventString + "]"

    def onApiCallResult(self, e):
        Logger().info("KPI events successfully submitted")
        while self._actionsSent:
            self._pendingActions.remove(self._actionsSent.pop())
        if self._stepByStep and not self._pendingActions:
            self._stepByStep = 0
        if not self.sendPendingEvents() and self._exiting:
            self.quit()  # Ensure quit method is defined

    def onApiCallError(self, e, response):
        if response.payload is None or response.payload.message == self.NORMAL_ERROR:
            return
        Logger().warn(
            f"Failed to submit KPIs: '{response.errorMessage}' with gameSessionId {self._actionsSent[0].gameSessionId} and event(s): {self.sentEventsToString()}"
        )
        if self._exiting:
            self._actionsSent.clear()
            self.storeData()
            if self._sentryReported:
                self.quit()
        else:
            firstAction = self._actionsSent.pop()
            if self._actionsSent:
                self._stepByStep = firstAction.gameSessionId
            else:
                self._pendingActions.remove(firstAction)
            self._actionsSent.clear()
            self.sendPendingEvents()

    def storeData(self):
        stats = [action.toString() for action in self._pendingActions]
        self._pendingActions.clear()
        savedStats = StoreDataManager().getData(self._dataStoreType, "statsActions")
        StoreDataManager().setData(self._dataStoreType, "statsActions", None)
        if savedStats:
            for savedStatsAction in savedStats:
                savedAction = StatsAction.fromString(savedStatsAction)
                if savedAction:
                    stats.append(savedAction)
        StoreDataManager().setData(self._dataStoreType, "statsActions", stats)

    def onUiLoaded(self, pEvent, uiTarget):
        removedIndex = 0
        uiStatsInfo = self._statsAssoc.get(uiTarget.name)
        if uiStatsInfo and (not uiStatsInfo.get('ftue') or self._firstTimeUserExperience.get(uiTarget.name)):
            self._stats[uiTarget.name] = uiStatsInfo['statClass'](uiTarget)
            removedIndex = self._removedStats.index(uiTarget.name) if uiTarget.name in self._removedStats else -1
            if removedIndex != -1:
                del self._stats[uiTarget.name]
                self._removedStats.pop(removedIndex)
    
    def onUiUnloadStart(self, pEvent, name):
        uiStats = self._stats.get(name)
        if uiStats:
            uiStats.remove()
        if name in self._stats:
            del self._stats[name]