from pydofus2.com.ankamagames.dofus.logic.game.common.spell.SpellModifier import SpellModifier
from pydofus2.com.ankamagames.dofus.logic.game.common.spell.SpellModifiers import SpellModifiers
from pydofus2.com.ankamagames.dofus.logic.game.common.spell.SpellModifierValueTypeEnum import (
    SpellModifierValueTypeEnum,
)
from pydofus2.com.ankamagames.dofus.network.enums.SpellModifierActionTypeEnum import SpellModifierActionTypeEnum
from pydofus2.com.ankamagames.dofus.network.types.game.character.spellmodifier.SpellModifierMessage import (
    SpellModifierMessage,
)
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton


class SpellModifiersManager(metaclass=Singleton):

    DATA_STORE_CATEGORY: str = "ComputerModule_spellModifiersManager"

    DATA_STORE_KEY_IS_VERBOSE: str = "spellModifiersManagerIsVerbose"

    DEFAULT_IS_VERBOSE: bool = False

    def __init__(self):
        self._entitiesMap = dict()
        self._isVerbose = self.DEFAULT_IS_VERBOSE
        super().__init__()

    @property
    def isVerbose(self) -> bool:
        return self._isVerbose

    @isVerbose.setter
    def isVerbose(self, isVerbose: bool) -> None:
        if self._isVerbose == isVerbose:
            return
        self._isVerbose = isVerbose
        verboseAction = "enabled" if self._isVerbose else "disabled"
        Logger().info(f"Verbose mode has been {verboseAction}")

    def setSpellModifiers(self, spellModifiers: SpellModifiers) -> bool:
        if spellModifiers is None:
            return False
        entityId = float(spellModifiers.entityId)
        spellId = float(spellModifiers.spellId)
        if entityId not in self._entitiesMap:
            self._entitiesMap[entityId] = dict[str, SpellModifiers]()
        self._entitiesMap[entityId][spellId] = spellModifiers
        return True

    def getSpellsModifiers(self, entityId: float):
        return self._entitiesMap.get(float(entityId))

    def getSpellModifiers(self, entityId: float, spellId: float) -> SpellModifiers:
        return self._entitiesMap.get(float(entityId), {}).get(float(spellId), None)

    def getSpellModifier(self, entityId: float, spellId: float, modifierId: float) -> SpellModifier:
        spellModifiers = self.getSpellModifiers(entityId, spellId)
        return spellModifiers.getModifier(modifierId) if spellModifiers else None

    def setRawSpellsModifiers(self, entityId: float, rawSpellsModifiers: list[SpellModifierMessage]):
        entityKey = float(entityId)
        spellsModifierStats = dict()
        self._entitiesMap[entityKey] = spellsModifierStats
        if rawSpellsModifiers:
            for rawSpellModifier in rawSpellsModifiers:
                self.internalSetRawSpellModifier(entityId, rawSpellModifier, spellsModifierStats)

    def setRawSpellModifier(self, entityId: float, rawSpellModifier: SpellModifierMessage):
        if rawSpellModifier is None:
            Logger().error("Tried to set a null raw spell modifier. Ignoring")

        entityKey = float(entityId)
        spellsModifierStats = self._entitiesMap.get(entityKey)

        if spellsModifierStats is None:
            spellsModifierStats = dict()
            self._entitiesMap[entityKey] = spellsModifierStats

        self.internalSetRawSpellModifier(entityId, rawSpellModifier, spellsModifierStats)

    def deleteSpellModifierAction(self, entityId: float, spellId: int, modifierType: int, actionType: int):
        spellModifiers = self.getSpellModifiers(entityId, spellId)

        if spellModifiers is None:
            Logger().error(
                f"Tried to delete spell {spellId} modifier {modifierType} (action: {actionType}) for entity with ID {entityId}, but no spells modifier stats were found. Aborting"
            )
            return

        spellModifiers.deleteModifierAction(modifierType, actionType)

    def deleteSpellModifiers(self, entityId: float, spellId: float) -> bool:
        entityKey = float(entityId)
        spellKey = float(spellId)
        if entityKey not in self._entitiesMap:
            Logger().error(
                f"Tried to del spell {spellKey}"
                + f" modifiers for entity with ID {entityKey}"
                + ", but no spells modifier stats were found. Aborting"
            )
            return False
        spellModifiers = self._entitiesMap[entityKey]
        if not spellModifiers or spellKey not in spellModifiers:
            Logger().error(
                f"Tried to del spell {spellKey}"
                + f" modifiers for entity with ID {entityKey}"
                + ", but none were found. Aborting"
            )
            return False
        del spellModifiers[spellKey]
        Logger().info(f"Spell {spellKey} modifiers for entity with ID {entityKey} deleted")
        return True

    def getModifiedBool(self, entityId: float, spellId: float, modifierType: int, baseValue: bool = False) -> bool:
        return self.getSpecificModifiedBool(entityId, spellId, modifierType, SpellModifierValueTypeEnum.ALL, baseValue)

    def getSpecificModifiedBool(
        self, entityId: float, spellId: float, modifierType: int, valueType: int = 1, baseValue: bool = False
    ) -> bool:
        spellModifiers = self.getSpellModifiers(entityId, spellId)
        return spellModifiers.getModifiedBool(modifierType, baseValue, valueType) if spellModifiers else baseValue

    def getModifiedInt(self, entityId: float, spellId: float, modifierType: int, baseValue: int = 0) -> int:
        return self.getSpecificModifiedInt(entityId, spellId, modifierType, SpellModifierValueTypeEnum.ALL, baseValue)

    def getSpecificModifiedInt(
        self, entityId: float, spellId: float, modifierType: int, valueType: int = 1, baseValue: int = 0
    ) -> int:
        spellModifiers = self.getSpellModifiers(entityId, spellId)
        return spellModifiers.getModifiedInt(modifierType, baseValue, valueType) if spellModifiers else baseValue

    def destroy(self):
        type(self)._singleton = None

    def internalSetRawSpellModifier(
        self, entityId: float, rawSpellModifier: SpellModifierMessage, spellsModifierStats: dict
    ):
        if not self.isValidActionType(rawSpellModifier.actionType):
            Logger().error("Tried to set an invalid raw spell modifier. Ignoring")
            return
        spellModifiers = spellsModifierStats.get(float(rawSpellModifier.spellId))
        if spellModifiers is None:
            spellModifiers = SpellModifiers(entityId, rawSpellModifier.spellId)
            self.setSpellModifiers(spellModifiers)
        spellModifier = spellModifiers.getModifier(rawSpellModifier.modifierType)
        if spellModifier is None:
            spellModifier = SpellModifier(rawSpellModifier.modifierType)
            spellModifiers.setModifier(spellModifier)
        spellModifier.applyAction(rawSpellModifier.actionType, rawSpellModifier.equipment, rawSpellModifier.context)

    def isValidActionType(self, actionType: int) -> bool:
        return actionType in [
            SpellModifierActionTypeEnum.ACTION_SET,
            SpellModifierActionTypeEnum.ACTION_BOOST,
            SpellModifierActionTypeEnum.ACTION_DEBOOST,
        ]
