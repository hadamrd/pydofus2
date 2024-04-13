from pydofus2.com.ankamagames.dofus.datacenter.alignments.AlignmentRank import AlignmentRank
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterionOperator import ItemCriterionOperator
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class SpecializationItemCriterion(ItemCriterion, IDataCenter):
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def text(self) -> str:
        readableCriterionValue: str = AlignmentRank.getAlignmentRankById(int(self._criterionValue)).name
        readableCriterionRef: str = I18n.getUiText("ui.alignment.sp�cialization")
        readableOperator: str = I18n.getUiText("ui.common.colon")
        if self._operator.text == ItemCriterionOperator.DIFFERENT:
            readableOperator = " " + I18n.getUiText("ui.common.differentFrom") + I18n.getUiText("ui.common.colon")
        return readableCriterionRef + readableOperator + readableCriterionValue

    def clone(self) -> IItemCriterion:
        return SpecializationItemCriterion(self.basicText)

    def getCriterion(self) -> int:
        return Kernel().alignmentFrame.playerRank
