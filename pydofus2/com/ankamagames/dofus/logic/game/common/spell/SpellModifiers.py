import pydofus2.com.ankamagames.dofus.logic.game.fight.managers.SpellModifiersManager as spellmm
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.game.common.spell.SpellModifier import \
    SpellModifier
from pydofus2.com.ankamagames.dofus.logic.game.fight.actions.UpdateSpellModifierAction import \
    UpdateSpellModifierAction
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger


class SpellModifiers:
    def __init__(self, entityId: float, spellId: float):
        super().__init__()
        self._entityId = entityId
        self._spellId = spellId
        self._modifiers = dict[str, SpellModifier]()

    @property
    def entityId(self) -> float:
        return self._entityId

    @property
    def spellId(self) -> float:
        return self._spellId

    @property
    def modifiers(self) -> dict:
        return self._modifiers

    @property
    def isVerbose(self) -> bool:
        return spellmm.SpellModifiersManager().isVerbose

    def getFormattedMessage(self, message: str) -> str:
        return (
            self.__class__.__name__
            + " (Entity ID: "
            + str(self._entityId)
            + ", Spell ID: "
            + str(self._spellId)
            + "): "
            + message
        )

    def setModifier(self, modifier: SpellModifier):
        modifier.entityId = self._entityId
        modifier.spellId = self._spellId
        self._modifiers[str(modifier.modifierType)] = modifier
        if self.isVerbose:
            Logger().info("Set modifier for entity with ID " + str(self.entityId) + " and spell with ID " + str(self.spellId) + ": " + modifier.dump())
        updateSpellModifierAction = UpdateSpellModifierAction.create(self.entityId, self.spellId, modifier.modifierType)
        Kernel().worker.process(updateSpellModifierAction)

    def getModifier(self, modifierType: int):
        if str(modifierType) not in self._modifiers:
            return None
        return self._modifiers[str(modifierType)]

    def deleteModifierAction(self, modifierType: int, actionType: int) -> None:        
        modifierKey: str = str(modifierType)
        if modifierKey not in self._modifiers:
            return
        modifier: SpellModifier = self._modifiers.get(modifierKey)
        if modifier is None:
            return
        modifier.removeAction(actionType)
        if modifier.isEmpty:
            del self._modifiers[modifierKey]
        if self.isVerbose:
            Logger().info(
                "Deleted modifier for entity with ID "
                + str(self._entityId)
                + " and spell with ID "
                + str(self._spellId)
                + ": "
                + modifier.dump()
            )

    def dump(self, indentLevel: int = 0) -> str:
        spellModifiersDump = ""
        spellModifierIds = [modifier.modifierType for modifier in self._modifiers.values()]
        spellModifierIds.sort()

        for spellModifierId in spellModifierIds:
            spellModifier = self._modifiers.get(str(spellModifierId))
            if spellModifier is not None:
                spellModifiersDump += "\n\t" + spellModifier.dump(indentLevel)

        if not spellModifiersDump:
            spellModifiersDump = "\n\tNo spell modifiers to display."

        return self.getFormattedMessage(spellModifiersDump)

    def getModifiedBool(self, modifierType: int, baseValue: bool = False, valueType: int = 1) -> bool:
        modifier = self._modifiers.get(str(modifierType))
        if modifier is None:
            return baseValue
        return modifier.getValueAsBool(valueType, baseValue)

    def getModifiedInt(self, modifierType: int, baseValue: int = 0, valueType: int = 1) -> int:
        modifier = self._modifiers.get(str(modifierType))
        if modifier is None:
            return baseValue
        return modifier.getValueAsInt(valueType, baseValue)

    def hasAction(self, modifierType: int, actionType: int) -> bool:
        modifier = self._modifiers.get(str(modifierType))
        if modifier is None:
            return False
        return modifier.hasAction(actionType)