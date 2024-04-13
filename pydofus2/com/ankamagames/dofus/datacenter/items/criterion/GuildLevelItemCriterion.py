from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class GuildLevelItemCriterion(ItemCriterion, IDataCenter):
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def text(self) -> str:
        readableCriterionValue: str = str(self._criterionValue)
        readableCriterionRef: str = I18n.getUiText("ui.guild.guildLevel")
        return readableCriterionRef + " " + self._operator.text + " " + readableCriterionValue

    def clone(self) -> IItemCriterion:
        return GuildLevelItemCriterion(self.basicText)

    def getCriterion(self) -> int:
        guild: GuildWrapper = Kernel().worker.getFrameByName("SocialFrame")
        if guild:
            return guild.level
        return 0
