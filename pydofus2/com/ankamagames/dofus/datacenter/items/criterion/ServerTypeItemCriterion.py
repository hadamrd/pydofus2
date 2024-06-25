from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import PlayerManager
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class ServerTypeItemCriterion(ItemCriterion, IDataCenter):
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def isRespected(self) -> bool:
        if self._operator.compare(PlayerManager().serverGameType, self._criterionValue):
            return True
        return False

    @property
    def text(self) -> str:
        return ""

    def clone(self) -> IItemCriterion:
        return ServerTypeItemCriterion(self.basicText)
