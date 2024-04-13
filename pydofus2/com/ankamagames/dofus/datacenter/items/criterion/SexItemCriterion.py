from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class SexItemCriterion(ItemCriterion, IDataCenter):
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def text(self) -> str:
        if self._criterionValue == 1:
            return I18n.getUiText("ui.tooltip.beFemale")
        return I18n.getUiText("ui.tooltip.beMale")

    def clone(self) -> IItemCriterion:
        return SexItemCriterion(self.basicText)

    def getCriterion(self) -> int:
        return int(PlayedCharacterManager().infos.sex)
