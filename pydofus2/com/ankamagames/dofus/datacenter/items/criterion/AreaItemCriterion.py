from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import \
    IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import \
    ItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterionOperator import \
    ItemCriterionOperator
from pydofus2.com.ankamagames.dofus.datacenter.world.Area import Area
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import \
    PlayedCharacterManager
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter


class AreaItemCriterion(ItemCriterion, IDataCenter):
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def isRespected(self) -> bool:
        if self.operator.text == ItemCriterionOperator.EQUAL or self.operator.text == ItemCriterionOperator.DIFFERENT:
            return super().isRespected()
        else:
            return False

    @property
    def text(self) -> str:
        readableCriterion: str = None
        area: Area = Area.getAreaById(self._criterionValue)
        if not area:
            return "error on AreaItemCriterion"
        areaName: str = area.name
        if self.operator.text == ItemCriterionOperator.EQUAL:
            readableCriterion = I18n.getUiText("ui.tooltip.beInArea", [areaName])
        if self.operator.text == ItemCriterionOperator.DIFFERENT:
            readableCriterion = I18n.getUiText("ui.tooltip.dontBeInArea", [areaName])
        return readableCriterion

    def clone(self) -> IItemCriterion:
        return AreaItemCriterion(self.basicText)

    def getCriterion(self) -> int:
        return PlayedCharacterManager().currentSubArea.area.id
