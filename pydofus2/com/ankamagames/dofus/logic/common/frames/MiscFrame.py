from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import PlayerManager
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.TimeManager import TimeManager
from pydofus2.com.ankamagames.dofus.misc.utils.HaapiKeyManager import HaapiKeyManager
from pydofus2.com.ankamagames.dofus.network.enums.ChatActivableChannelsEnum import ChatActivableChannelsEnum
from pydofus2.com.ankamagames.dofus.network.enums.HaapiAuthEnum import HaapiAuthTypeEnum
from pydofus2.com.ankamagames.dofus.network.enums.HaapiSessionTypeEnum import HaapiSessionTypeEnum
from pydofus2.com.ankamagames.dofus.network.enums.SubscriptionRequiredEnum import SubscriptionRequiredEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.approach.ServerSessionConstantsMessage import (
    ServerSessionConstantsMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.approach.ServerSettingsMessage import ServerSettingsMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.basic.CurrentServerStatusUpdateMessage import (
    CurrentServerStatusUpdateMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.houses.AccountHouseMessage import (
    AccountHouseMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.subscriber.SubscriptionLimitationMessage import (
    SubscriptionLimitationMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.web.haapi.HaapiApiKeyMessage import HaapiApiKeyMessage
from pydofus2.com.ankamagames.dofus.network.messages.web.haapi.HaapiAuthErrorMessage import HaapiAuthErrorMessage
from pydofus2.com.ankamagames.dofus.network.messages.web.haapi.HaapiSessionMessage import HaapiSessionMessage
from pydofus2.com.ankamagames.dofus.network.types.game.approach.ServerSessionConstantInteger import (
    ServerSessionConstantInteger,
)
from pydofus2.com.ankamagames.dofus.network.types.game.approach.ServerSessionConstantLong import (
    ServerSessionConstantLong,
)
from pydofus2.com.ankamagames.dofus.network.types.game.approach.ServerSessionConstantString import (
    ServerSessionConstantString,
)
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority


class MiscFrame(Frame, metaclass=Singleton):

    SERVER_CONST_TIME_BEFORE_DISCONNECTION: int = 1

    SERVER_CONST_KOH_DURATION: int = 2

    SERVER_CONST_KOH_WINNING_SCORE: int = 3

    SERVER_CONST_MINIMAL_TIME_BEFORE_KOH: int = 4

    SERVER_CONST_TIME_BEFORE_WEIGH_IN_KOH: int = 5

    _serverSessionConstants: dict

    _mouseOnStage: bool = True

    _serverStatus: int

    def __init__(self):
        super().__init__()

    def pushed(self) -> bool:
        self._serverSessionConstants = dict()
        return True

    def pulled(self) -> bool:
        return True

    def getServerSessionConstant(self, id: int) -> object:
        return self._serverSessionConstants[id]

    def getServerStatus(self) -> int:
        return self._serverStatus

    def process(self, msg: Message) -> bool:

        if isinstance(msg, ServerSettingsMessage):
            ssmsg = msg
            PlayerManager().serverCommunityId = ssmsg.community
            PlayerManager().serverLang = ssmsg.lang
            PlayerManager().serverGameType = ssmsg.gameType
            PlayerManager().serverIsMonoAccount = ssmsg.isMonoAccount
            PlayerManager().arenaLeaveBanTime = ssmsg.arenaLeaveBanTime
            PlayerManager().hasFreeAutopilot = ssmsg.hasFreeAutopilot
            return True

        if isinstance(msg, ServerSessionConstantsMessage):
            sscmsg = msg
            self._serverSessionConstants = dict()
            for constant in sscmsg.variables:
                if isinstance(constant, ServerSessionConstantInteger):
                    self._serverSessionConstants[constant.id] = constant.value
                elif isinstance(constant, ServerSessionConstantLong):
                    self._serverSessionConstants[constant.id] = constant.value
                elif isinstance(constant, ServerSessionConstantString):
                    self._serverSessionConstants[constant.id] = constant.value
                else:
                    self._serverSessionConstants[constant.id] = None
            return True

        if isinstance(msg, CurrentServerStatusUpdateMessage):
            cssum = msg
            self._serverStatus = cssum.status
            return True

        if isinstance(msg, AccountHouseMessage):
            pass
            # if not Kernel().worker.getFrame('HouseFrame'):
            #     Kernel.worker.addFrame(HouseFrame())
            # houseFrame = Kernel().worker.getFrame('HouseFrame')
            # if houseFrame is not None:
            #     houseFrame.process(msg)
            return True

        if isinstance(msg, HaapiSessionMessage):
            Logger().debug(f"HaapiSessionMessage received : {msg.key}")
            if msg.type == HaapiSessionTypeEnum.HAAPI_ACCOUNT_SESSION:
                HaapiKeyManager().saveAccountSessionId(msg.key)
            elif msg.type == HaapiSessionTypeEnum.HAAPI_GAME_SESSION:
                HaapiKeyManager().saveGameSessionId(msg.key)
            else:
                return False
            return True

        if isinstance(msg, HaapiApiKeyMessage):
            logStr = "RECEIVED API KEY : "
            if msg.token is not None and len(msg.token) >= 5:
                logStr += msg.token[:5]
            Logger().debug(logStr)
            KernelEventsManager().send(KernelEvent.HaapiApiKeyReady, msg.token)
            return True

        if isinstance(msg, HaapiAuthErrorMessage):
            Logger().debug(f"ERROR ON ASKING API KEY type={msg.type}, id={msg.getMessageId()}")
            if msg.type == HaapiAuthTypeEnum.HAAPI_API_KEY:
                Logger().error("Error during ApiKey request.")
            return True

        if isinstance(msg, SubscriptionLimitationMessage):
            Logger().error("SubscriptionLimitationMessage reason " + msg.reason)
            text = ""
            payZonePopupMode = "payzone"
            if msg.reason == SubscriptionRequiredEnum.LIMIT_ON_JOB_XP:
                text = I18n.getUiText("ui.payzone.limitJobXp")
                payZonePopupMode = "payzone_job"
            if msg.reason == SubscriptionRequiredEnum.LIMIT_ON_JOB_USE:
                text = I18n.getUiText("ui.payzone.limitJobXp")
                payZonePopupMode = "payzone_job"

            if msg.reason == SubscriptionRequiredEnum.LIMIT_ON_MAP:
                text = I18n.getUiText("ui.payzone.limit")

            if msg.reason == SubscriptionRequiredEnum.LIMIT_ON_ITEM:
                text = I18n.getUiText("ui.payzone.limitItem")

            if msg.reason == SubscriptionRequiredEnum.LIMIT_ON_HAVENBAG:
                text = I18n.getUiText("ui.payzone.limit")
                payZonePopupMode = "payzone_havenbag"
            else:
                text = I18n.getUiText("ui.payzone.limit")

            Logger().warning("SubscriptionLimitationMessage text " + text)
            KernelEventsManager().send(
                KernelEvent.TextInformation,
                text,
                ChatActivableChannelsEnum.PSEUDO_CHANNEL_INFO,
                TimeManager().getTimestamp(),
            )
            KernelEventsManager().send(KernelEvent.NonSubscriberPopup, [payZonePopupMode])
            return True

    @property
    def priority(self) -> int:
        return Priority.LOW
