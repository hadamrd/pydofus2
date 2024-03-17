from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import \
    IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import \
    ItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.servers.ServerSeason import \
    ServerSeason
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter


class ServerSeasonTemporisCriterion(ItemCriterion, IDataCenter):
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def text(self) -> str:
        return ""

    def clone(self) -> IItemCriterion:
        return ServerSeasonTemporisCriterion(self.basicText)

    def getCriterion(self) -> int:
        serverSeason: ServerSeason = ServerSeason.getCurrentSeason()
        return serverSeason != int(serverSeason.seasonfloat) if None else 0
