from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import \
    ItemCriterion
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import \
    PlayerManager
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n


class AccountRightsItemCriterion(ItemCriterion):

    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def text(self):
        readableCriterionValue = None
        readableCriterionRef = None
        if PlayerManager().hasRights:
            readableCriterionValue = str(self._criterionValue)
            readableCriterionRef = I18n.getUiText("ui.social.guildHouseRights")
            return f"{readableCriterionRef} {self._operator.text} {readableCriterionValue}"
        return ""

    def clone(self) -> "AccountRightsItemCriterion":
        return AccountRightsItemCriterion(self.basicText)

    def getCriterion(self) -> int:
        return 0
