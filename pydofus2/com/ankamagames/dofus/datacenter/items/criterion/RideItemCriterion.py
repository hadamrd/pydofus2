from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterionOperator import ItemCriterionOperator
from pydofus2.com.ankamagames.dofus.datacenter.mounts.Mount import Mount
from pydofus2.com.ankamagames.dofus.internalDatacenter.mount.MountData import MountData
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class RideItemCriterion(ItemCriterion, IDataCenter):
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def text(self) -> str:
        readableCriterion: str = None
        mountModel: Mount = Mount.getMountById(self._criterionValue)
        if self._criterionValue == 0 or not mountModel:
            return ""
        if self._operator.text == ItemCriterionOperator.EQUAL:
            readableCriterion = I18n.getUiText("ui.tooltip.mountEquiped", [mountModel.name])
        elif self._operator.text == ItemCriterionOperator.DIFFERENT:
            readableCriterion = I18n.getUiText("ui.tooltip.mountNonEquiped", [mountModel.name])
        return readableCriterion

    def clone(self) -> IItemCriterion:
        return RideItemCriterion(self.basicText)

    def getCriterion(self) -> int:
        mountId: int = 0
        mount: MountData = PlayedCharacterManager().mount
        if mount and PlayedCharacterManager().isRidding:
            mountId = mount.modelId
        return mountId
