from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.IItemCriterion import IItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterion import ItemCriterion
from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.ItemCriterionOperator import ItemCriterionOperator
from pydofus2.com.ankamagames.dofus.datacenter.spells.Spell import Spell
from pydofus2.com.ankamagames.dofus.internalDatacenter.spells.SpellWrapper import SpellWrapper
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import PlayedCharacterManager
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class SpellItemCriterion(ItemCriterion, IDataCenter):

    _spellId: int

    def __init__(self, pCriterion: str):
        super().__init__(pCriterion)
        arrayParams: list = str(self._criterionValueText).split(",")
        if arrayParams and len(arrayParams) > 0:
            if len(arrayParams) <= 1:
                self._spellId = int(arrayParams[0])
        else:
            self._spellId = int(self._criterionValue)

    @property
    def isRespected(self) -> bool:
        sp: SpellWrapper = None
        for sp in PlayedCharacterManager().playerSpellList:
            if sp.id == self._spellId:
                if self._operator.text == ItemCriterionOperator.EQUAL:
                    return True
                return False
        if self._operator.text == ItemCriterionOperator.DIFFERENT:
            return True
        return False

    @property
    def text(self) -> str:
        readableCriterion: str = ""
        spell: Spell = Spell.getSpellById(self._spellId)
        if not spell:
            return readableCriterion
        readableCriterionValue: str = spell.name
        if self._operator.text == ItemCriterionOperator.EQUAL:
            readableCriterion = I18n.getUiText("ui.criterion.gotSpell", [readableCriterionValue])
        elif self._operator.text == ItemCriterionOperator.DIFFERENT:
            readableCriterion = I18n.getUiText("ui.criterion.doesntGotSpell", [readableCriterionValue])
        return readableCriterion

    def clone(self) -> IItemCriterion:
        return SpellItemCriterion(self.basicText)
