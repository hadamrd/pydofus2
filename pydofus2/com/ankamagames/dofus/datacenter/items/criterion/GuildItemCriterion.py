from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class GuildItemCriterion(ItemCriterion, IDataCenter):
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def text(self) -> str:
        if self._criterionValue == 0:
            return I18n.getUiText("ui.criterion.noguild")
        return I18n.getUiText("ui.criterion.hasGuild")

    def clone(self) -> IItemCriterion:
        return GuildItemCriterion(self.basicText)

    def getCriterion(self) -> int:
        guild: GuildWrapper = Kernel().worker.getFrame("SocialFrame")
        if guild:
            return 1
        return 0
