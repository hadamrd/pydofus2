from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import \
    IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import \
    ItemCriterion
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter


class AllianceItemCriterion(ItemCriterion, IDataCenter):
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def text(self) -> str:
        if self._criterionValue == 0:
            return I18n.getUiText("ui.criterion.noAlliance")
        return I18n.getUiText("ui.criterion.hasAlliance")

    def clone(self) -> IItemCriterion:
        return AllianceItemCriterion(self.basicText)

    def getCriterion(self) -> int:
        raise NotImplementedError()
        alliance: AllianceWrapper = AllianceFrame().alliance
        if alliance:
            return 1
        return 0
