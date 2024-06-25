from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.servers.Server import Server
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import PlayerManager
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class ServerItemCriterion(ItemCriterion, IDataCenter):
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def text(self) -> str:
        readableCriterionValue: str = Server.getServerById(self._criterionValue).name
        readableCriterionRef: str = I18n.getUiText("ui.header.server")
        return readableCriterionRef + " " + self._operator.text + " " + readableCriterionValue

    def clone(self) -> IItemCriterion:
        return ServerItemCriterion(self.basicText)

    def getCriterion(self) -> int:
        return PlayerManager().server.id
