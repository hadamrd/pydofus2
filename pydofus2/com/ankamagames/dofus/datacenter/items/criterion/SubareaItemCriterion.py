from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterionOperator import ItemCriterionOperator
from pydofus2.com.ankamagames.dofus.datacenter.world.SubArea import SubArea
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n


class SubareaItemCriterion(ItemCriterion):
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def isRespected(self) -> bool:
        PlayedCharacterManager().currentSubArea.id
        if self._operator.text in [ItemCriterionOperator.EQUAL, ItemCriterionOperator.DIFFERENT]:
            return super().isRespected
        else:
            return False

    @property
    def text(self) -> str:
        readableCriterion: str = None
        subArea: SubArea = SubArea.getSubAreaById(self._criterionValue)
        if not subArea:
            return "error on subareaItemCriterion"
        zoneName = subArea.name
        if self._operator.text == ItemCriterionOperator.EQUAL:
            readableCriterion = I18n.getUiText("ui.tooltip.beInSubarea", [zoneName])
        if self._operator.text == ItemCriterionOperator.DIFFERENT:
            readableCriterion = I18n.getUiText("ui.tooltip.dontBeInSubarea", [zoneName])
        return readableCriterion

    def clone(self) -> IItemCriterion:
        return SubareaItemCriterion(self.basicText)

    def getCriterion(self) -> int:
        return PlayedCharacterManager().currentSubArea.id
