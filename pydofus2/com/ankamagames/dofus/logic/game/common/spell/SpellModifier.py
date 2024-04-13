from pydofus2.com.ankamagames.dofus.logic.game.common.spell.SpellModifierValueTypeEnum import (
    SpellModifierValueTypeEnum,
)
from pydofus2.com.ankamagames.dofus.network.enums.SpellModifierActionTypeEnum import SpellModifierActionTypeEnum
from pydofus2.com.ankamagames.dofus.network.enums.SpellModifierTypeEnum import SpellModifierTypeEnum


class SpellModifier:

    UNKNOWN_MODIFIER_NAME: str = "unknown"

    _entityId: float = None

    _spellId: float = None

    _modifierType = 0

    _name: str = None

    _actions: dict[int, "SpellModifierAction"]

    def __init__(self, modifierType: float):
        self._actions = dict()
        super().__init__()
        self._modifierType = modifierType

    @property
    def modifierType(self) -> float:
        return self._modifierType

    @property
    def isEmpty(self):
        return not self._actions

    def hasAction(self, actionType: int):
        return str(actionType) in self._actions

    def applyAction(self, actionType, equipment: int, context: int):
        action: SpellModifierAction = SpellModifierAction(actionType, equipment, context)
        self._actions[action.actionType] = action

    def removeAction(self, actionType: int):
        key: str = str(actionType)
        if key in self._actions:
            del self._actions[key]

    def getValueAsInt(self, valueType: int = 1, baseValue: int = 0) -> int:
        setAction: SpellModifierAction = self._actions.get(SpellModifierActionTypeEnum.ACTION_SET)
        if setAction:
            return setAction.getInt(valueType)
        boostAction = self._actions.get(SpellModifierActionTypeEnum.ACTION_BOOST)
        deboostAction = self._actions.get(SpellModifierActionTypeEnum.ACTION_DEBOOST)
        boostValue = boostAction.getInt(valueType) if boostAction else 0
        deboostValue = deboostAction.getInt(valueType) if deboostAction else 0
        modifierValue = boostValue - deboostValue
        return baseValue + modifierValue * self.getIntModifierSign()

    def getValueAsBool(self, valueType=1, baseValue=False):
        flag = False

        setAction = self._actions.get(SpellModifierActionTypeEnum.ACTION_SET)
        if setAction:
            return setAction.getBool(valueType)

        boostAction = self._actions.get(SpellModifierActionTypeEnum.ACTION_BOOST)
        deboostAction = self._actions.get(SpellModifierActionTypeEnum.ACTION_DEBOOST)

        boostValue = boostAction.getBool(valueType) if boostAction else False
        deboostValue = deboostAction.getBool(valueType) if deboostAction else False

        if boostValue and deboostValue:
            flag = baseValue
        elif boostValue:
            flag = True
        elif deboostValue:
            flag = False
        else:
            flag = baseValue

        return flag

    def getIntModifierSign(self):
        if self._modifierType == SpellModifierTypeEnum.AP_COST:
            return -1
        elif self._modifierType == SpellModifierTypeEnum.CAST_INTERVAL:
            return -1
        else:
            return 1

    @property
    def entityId(self) -> float:
        return self._entityId

    @entityId.setter
    def entityId(self, entityId: float) -> None:
        self._entityId = entityId

    @property
    def spellId(self) -> float:
        return self._spellId

    @spellId.setter
    def spellId(self, spellId: float) -> None:
        self._spellId = spellId

    @property
    def id(self) -> float:
        return self._id

    @property
    def baseValue(self) -> float:
        return self._baseValue

    @property
    def additionalValue(self) -> float:
        return self._additionalValue

    @property
    def objectsAndMountBonusValue(self) -> float:
        return self._objectsAndMountBonusValue

    @property
    def alignGiftBonusValue(self) -> float:
        return self._alignGiftBonusValue

    @property
    def contextModifValue(self) -> float:
        return self._contextModifValue

    @property
    def totalValue(self) -> float:
        return self._totalValue

    def getModifierName(self) -> str:
        if self._id == SpellModifierTypeEnum.INVALID_MODIFICATION:
            return "invalid modification"
        if self._id == SpellModifierTypeEnum.RANGEABLE:
            return "rangeable"
        if self._id == SpellModifierTypeEnum.DAMAGE:
            return "damage"
        if self._id == SpellModifierTypeEnum.BASE_DAMAGE:
            return "base damage"
        if self._id == SpellModifierTypeEnum.HEAL_BONUS:
            return "heal bonus"
        if self._id == SpellModifierTypeEnum.AP_COST:
            return "ap cost"
        if self._id == SpellModifierTypeEnum.CAST_INTERVAL:
            return "cast interval"
        if self._id == SpellModifierTypeEnum.CRITICAL_HIT_BONUS:
            return "critical hit bonus"
        if self._id == SpellModifierTypeEnum.CAST_LINE:
            return "cast line"
        if self._id == SpellModifierTypeEnum.LOS:
            return "los"
        if self._id == SpellModifierTypeEnum.MAX_CAST_PER_TURN:
            return "max cast per turn"
        if self._id == SpellModifierTypeEnum.MAX_CAST_PER_TARGET:
            return "max cast per target"
        if self._id == SpellModifierTypeEnum.RANGE_MAX:
            return "range max"
        if self._id == SpellModifierTypeEnum.RANGE_MIN:
            return "range min"
        if self._id == SpellModifierTypeEnum.OCCUPIED_CELL:
            return "occupied cell"
        if self._id == SpellModifierTypeEnum.FREE_CELL:
            return "free cell"
        if self._id == SpellModifierTypeEnum.VISIBLE_TARGET:
            return "visible target"
        if self._id == SpellModifierTypeEnum.PORTAL_PROJECTION:
            return "portal projection"
        if self._id == SpellModifierTypeEnum.PORTAL_FREE_CELL:
            return "portal free cell"
        else:
            return self.UNKNOWN_MODIFIER_NAME

    def dump(self, indentLevel=0):
        indent = "\t" * indentLevel
        className = self.__class__.__name__  # This gets the name of the current instance's class in Python
        toReturn = f"{className} {self._name} (Entity ID: {self._entityId}, Spell ID: {self._spellId}, type: {self._modifierType})"

        actionTypes = [action.actionType for action in self._actions.values()]
        actionTypes.sort()

        for actionType in actionTypes:
            action = self._actions[actionType]
            toReturn += f"\n{indent}{action.dump(self.isBool())}"

        return toReturn

    def isBool(self):
        return self._modifierType in [
            SpellModifierTypeEnum.RANGEABLE,
            SpellModifierTypeEnum.CAST_LINE,
            SpellModifierTypeEnum.LOS,
            SpellModifierTypeEnum.OCCUPIED_CELL,
            SpellModifierTypeEnum.FREE_CELL,
            SpellModifierTypeEnum.VISIBLE_TARGET,
            SpellModifierTypeEnum.PORTAL_PROJECTION,
            SpellModifierTypeEnum.PORTAL_FREE_CELL,
        ]


class SpellModifierAction:

    def __init__(self, actionType, equipment, context):
        self._actionType = actionType
        self._equipment = equipment
        self._context = context
        self._total = self._equipment + self._context

    @property
    def actionType(self):
        return self._actionType

    def getEquipmentAsInt(self):
        return self._equipment

    def getEquipmentAsBool(self):
        return self._equipment > 0

    def getContextAsInt(self):
        return self._context

    def getContextAsBool(self):
        return self._context > 0

    def getTotalAsInt(self):
        return self._total

    def getTotalAsBool(self):
        return self._total > 0

    def getInt(self, valueType):
        if valueType == SpellModifierValueTypeEnum.ALL:
            return self.getTotalAsInt()
        elif valueType == SpellModifierValueTypeEnum.EQUIPMENT:
            return self.getEquipmentAsInt()
        elif valueType == SpellModifierValueTypeEnum.CONTEXT:
            return self.getContextAsInt()
        else:
            return 0

    def getBool(self, valueType):
        if valueType == SpellModifierValueTypeEnum.ALL:
            return self.getTotalAsBool()
        elif valueType == SpellModifierValueTypeEnum.EQUIPMENT:
            return self.getEquipmentAsBool()
        elif valueType == SpellModifierValueTypeEnum.CONTEXT:
            return self.getContextAsBool()
        else:
            return False

    def dump(self, asBool=False):
        equipmentStr = str(self.getEquipmentAsInt())
        contextStr = str(self.getContextAsInt())
        totalStr = str(self.getTotalAsInt())
        if asBool:
            equipmentStr += " (" + str(self.getEquipmentAsBool()) + ")"
            contextStr += " (" + str(self.getContextAsBool()) + ")"
            totalStr += " (" + str(self.getTotalAsBool()) + ")"
        return (
            self.getActionName()
            + "["
            + "equipment: "
            + equipmentStr
            + ", context: "
            + contextStr
            + ", total: "
            + totalStr
            + "]"
        )

    def getActionName(self):
        if self._actionType == SpellModifierActionTypeEnum.ACTION_SET:
            return "Set"
        elif self._actionType == SpellModifierActionTypeEnum.ACTION_BOOST:
            return "Boost"
        elif self._actionType == SpellModifierActionTypeEnum.ACTION_DEBOOST:
            return "Deboost"
        elif self._actionType == SpellModifierActionTypeEnum.ACTION_INVALID:
            return "Invalid"
        else:
            return "???"
