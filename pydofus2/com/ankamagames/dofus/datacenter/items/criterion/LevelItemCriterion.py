from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterionOperator import ItemCriterionOperator
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class LevelItemCriterion(ItemCriterion, IDataCenter):
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def text(self) -> str:
        readableCriterionValue: str = str(self._criterionValue)
        readableCriterionRef: str = I18n.getUiText("ui.common.level")
        if self._operator.text == ItemCriterionOperator.SUPERIOR:
            return I18n.getUiText("ui.common.minimumLevelCondition", [(self._criterionValue + 1)])
        if self._operator.text == ItemCriterionOperator.INFERIOR:
            return I18n.getUiText("ui.common.maximumLevelCondition", [(self._criterionValue - 1)])
        return readableCriterionRef + " " + self._operator.text + " " + readableCriterionValue

    def clone(self) -> IItemCriterion:
        return LevelItemCriterion(self.basicText)

    def getCriterion(self) -> int:
        return PlayedCharacterManager().limitedLevel
