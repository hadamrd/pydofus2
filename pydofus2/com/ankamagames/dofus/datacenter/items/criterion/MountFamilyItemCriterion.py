from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterionOperator import ItemCriterionOperator
from pydofus2.com.ankamagames.dofus.datacenter.mounts.MountFamily import MountFamily
from pydofus2.com.ankamagames.dofus.internalDatacenter.mount.MountData import MountData
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class MountFamilyItemCriterion(ItemCriterion, IDataCenter):
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def text(self) -> str:
        readableCriterionRef: str = None
        mountFamily: MountFamily = MountFamily.getMountFamilyById(float(self._criterionValue))
        if not mountFamily:
            readableCriterionRef = "???"
        else:
            readableCriterionRef = mountFamily.name
        if self._operator.text == ItemCriterionOperator.EQUAL:
            return I18n.getUiText("ui.tooltip.mountEquipedFamily", [readableCriterionRef])
        if self._operator.text == ItemCriterionOperator.DIFFERENT:
            return I18n.getUiText("ui.tooltip.mountNonEquipedFamily", [readableCriterionRef])
        return ""

    def clone(self) -> IItemCriterion:
        return MountFamilyItemCriterion(self.basicText)

    def getCriterion(self) -> int:
        mount: MountData = PlayedCharacterManager().mount
        if not mount or not PlayedCharacterManager().isRidding:
            return -1
        return mount.model.familyId
