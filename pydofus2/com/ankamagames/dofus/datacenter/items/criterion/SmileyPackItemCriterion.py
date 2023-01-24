from pydofus2.com.ankamagames.dofus.datacenter.communication.SmileyPack import SmileyPack
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterionOperator import ItemCriterionOperator
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class SmileyPackItemCriterion(ItemCriterion, IDataCenter):
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def isRespected(self) -> bool:
        pack: SmileyPack = None
        packList: list = Kernel().worker.getFrame("ChatFrame")
        for pack in packList:
            if pack.id == self._criterionValue:
                return False
        return True

    @property
    def text(self) -> str:
        readableCriterion: str = None
        if self._operator.text == ItemCriterionOperator.DIFFERENT:
            readableCriterion = I18n.getUiText("ui.tooltip.dontPossessSmileyPack")
        else:
            readableCriterion = I18n.getUiText("ui.tooltip.possessSmileyPack")
        return (
            readableCriterion
            + " '"
            + SmileyPack.getSmileyPackById(self._criterionValue).name
            + "'"
        )

    def clone(self) -> IItemCriterion:
        return SmileyPackItemCriterion(self.basicText)

    def getCriterion(self) -> int:
        pack: SmileyPack = None
        packList: list = Kernel().worker.getFrame("ChatFrame")
        for pack in packList:
            if pack.id == self._criterionValue:
                return 1
        return 0
