from pydofus2.com.ankamagames.dofus.datacenter.breeds.Breed import Breed
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterionOperator import ItemCriterionOperator
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class BreedItemCriterion(ItemCriterion, IDataCenter):

    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def text(self) -> str:
        readableCriterionRef: str = Breed.getBreedById(float(self._criterionValue)).shortName
        if self._operator.text == ItemCriterionOperator.EQUAL:
            return I18n.getUiText("ui.tooltip.beABreed", [readableCriterionRef])
        if self._operator.text == ItemCriterionOperator.DIFFERENT:
            return I18n.getUiText("ui.tooltip.dontBeABreed", [readableCriterionRef])
        return ""

    def clone(self) -> IItemCriterion:
        return BreedItemCriterion(self.basicText)

    def getCriterion(self) -> int:
        return int(PlayedCharacterManager().infos.breed)
