from pydofus2.com.ankamagames.dofus.logic.common.managers.InterClientManager import \
    InterClientManager
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import \
    PlayerManager
from pydofus2.com.ankamagames.dofus.misc.stats.IHookStats import IHookStats
from pydofus2.com.ankamagames.dofus.misc.stats.InternalStatisticEnum import \
    InternalStatisticTypeEnum
from pydofus2.com.ankamagames.dofus.misc.stats.IStatsClass import IStatsClass
from pydofus2.com.ankamagames.dofus.misc.stats.StatsAction import StatsAction
from pydofus2.com.ankamagames.dofus.misc.utils.HaapiKeyManager import \
    HaapiKeyManager
from pydofus2.com.ankamagames.jerakine.managers.OptionManager import \
    OptionManager


class SessionEndStats(IHookStats, IStatsClass):

    def __init__(self):
        super().__init__()
        action = StatsAction(InternalStatisticTypeEnum.END_SESSION)
        action.user = StatsAction.getUserId()
        action.gameSessionId = HaapiKeyManager().getGameSessionId()
        action.setParam("account_id", PlayerManager().accountId)
        action.setParam("screen_size", 17)
        action.setParam("quality", 0)
        action.setParam("force_cpu", False)
        action.setParam("client_open", InterClientManager().numClients)
        action.setParam("damage_preview", True)
        action.send()

    def onHook(self, pHook, pArgs):
        pass

    def process(self, pMessage, pArgs=None):
        pass

    def remove(self):
        pass
