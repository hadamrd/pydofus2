from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import \
    IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import \
    ItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterionOperator import \
    ItemCriterionOperator
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.FightersStateManager import \
    FightersStateManager
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter


class StateCriterion(ItemCriterion, IDataCenter):
    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)

    @property
    def isRespected(self) -> bool:
        from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.CurrentPlayedFighterManager import \
            CurrentPlayedFighterManager

        states: list = FightersStateManager().getStates(CurrentPlayedFighterManager().currentFighterId)
        if self._operator.text == ItemCriterionOperator.EQUAL:
            return self.criterionValue in states
        if self._operator.text == ItemCriterionOperator.DIFFERENT:
            return self.criterionValue not in states
        else:
            return False

    def clone(self) -> "IItemCriterion":
        return StateCriterion(self.basicText)
