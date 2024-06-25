from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import (
        IItemCriterion,
    )

from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.dofus.network.types.game.character.alignment.ActorExtendedAlignmentInformations import (
    ActorExtendedAlignmentInformations,
)
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n


class AlignmentLevelItemCriterion(ItemCriterion, IDataCenter):

    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def text(self) -> str:
        readableCriterionRef = I18n.getUiText("ui.tooltip.AlignmentLevel")
        return readableCriterionRef + " " + self._operator.text + " " + self._criterionValue

    def clone(self) -> "IItemCriterion":
        return AlignmentLevelItemCriterion(self.basicText)

    def getCriterion(self) -> int:
        alignInfo: ActorExtendedAlignmentInformations = PlayedCharacterManager().characteristics.alignmentInfos
        return alignInfo.alignmentValue
