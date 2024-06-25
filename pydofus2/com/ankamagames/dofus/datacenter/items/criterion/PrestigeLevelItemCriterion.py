from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.network.ProtocolConstantsEnum import ProtocolConstantsEnum
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class PrestigeLevelItemCriterion(ItemCriterion, IDataCenter):
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def text(self) -> str:
        readableCriterionValue: str = str(self._criterionValue)
        readableCriterionRef: str = I18n.getUiText("ui.common.prestige")
        return f"{readableCriterionRef} {self._operator.text} {readableCriterionValue}"

    def clone(self) -> IItemCriterion:
        return PrestigeLevelItemCriterion(self.basicText)

    def getCriterion(self) -> int:
        prestige = 0
        if PlayedCharacterManager().infos.level > ProtocolConstantsEnum.MAX_LEVEL:
            prestige = PlayedCharacterManager().infos.level - ProtocolConstantsEnum.MAX_LEVEL
        return prestige
