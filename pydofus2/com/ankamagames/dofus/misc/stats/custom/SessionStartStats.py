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


class SessionStartStats(IHookStats, IStatsClass):

    def __init__(self):
        super().__init__()
        action = StatsAction(InternalStatisticTypeEnum.START_SESSION)
        action.user = StatsAction.getUserId()
        action.gameSessionId = HaapiKeyManager().getGameSessionId()
        action.setParam("account_id", PlayerManager().accountId)
        action.setParam("client_open", InterClientManager().numClients)
        action.send()

    def onHook(self, pHook, pArgs):
        pass

    def process(self, pMessage, pArgs=None):
        pass

    def remove(self):
        pass
