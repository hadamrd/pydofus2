from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class BonesItemCriterion(ItemCriterion, IDataCenter):
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def text(self) -> str:
        if self._criterionValue == 0 and self._criterionValueText == "B":
            return I18n.getUiText("ui.criterion.initialBones")
        return I18n.getUiText("ui.criterion.bones") + " " + self._operator.text + " " + str(self._criterionValue)

    @property
    def isRespected(self) -> bool:
        if self._criterionValue == 0 and self._criterionValueText == "B":
            return PlayedCharacterManager().infos.entityLook.bonesId == 1
        return PlayedCharacterManager().infos.entityLook.bonesId == self._criterionValue

    def clone(self) -> IItemCriterion:
        return BonesItemCriterion(self.basicText)

    def getCriterion(self) -> int:
        return PlayedCharacterManager().infos.entityLook.bonesId
