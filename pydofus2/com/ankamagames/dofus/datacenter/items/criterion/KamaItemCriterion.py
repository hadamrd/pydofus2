from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class KamaItemCriterion(ItemCriterion, IDataCenter):
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def text(self) -> str:
        readableCriterionRef: str = I18n.getUiText("ui.common.kamas")
        return readableCriterionRef + " " + self._operator.text + " " + self._criterionValue

    @property
    def isRespected(self) -> bool:
        return self._operator.compare(PlayedCharacterManager().characteristics.kamas, self._criterionValue)

    def clone(self) -> IItemCriterion:
        return KamaItemCriterion(self.basicText)
