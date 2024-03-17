from pydofus2.com.ankamagames.dofus.datacenter.effects.EffectInstance import \
    EffectInstance
from pydofus2.com.ankamagames.dofus.datacenter.effects.instances.EffectInstanceCreature import \
    EffectInstanceCreature
from pydofus2.com.ankamagames.dofus.datacenter.effects.instances.EffectInstanceDate import \
    EffectInstanceDate
from pydofus2.com.ankamagames.dofus.datacenter.effects.instances.EffectInstanceDice import \
    EffectInstanceDice
from pydofus2.com.ankamagames.dofus.datacenter.effects.instances.EffectInstanceDuration import \
    EffectInstanceDuration
from pydofus2.com.ankamagames.dofus.datacenter.effects.instances.EffectInstanceInteger import \
    EffectInstanceInteger
from pydofus2.com.ankamagames.dofus.datacenter.effects.instances.EffectInstanceLadder import \
    EffectInstanceLadder
from pydofus2.com.ankamagames.dofus.datacenter.effects.instances.EffectInstanceMinMax import \
    EffectInstanceMinMax
from pydofus2.com.ankamagames.dofus.datacenter.effects.instances.EffectInstanceMount import \
    EffectInstanceMount
from pydofus2.com.ankamagames.dofus.datacenter.effects.instances.EffectInstanceString import \
    EffectInstanceString
from pydofus2.com.ankamagames.dofus.datacenter.items.IncarnationLevel import \
    IncarnationLevel
from pydofus2.com.ankamagames.dofus.enums.ActionIds import ActionIds
from pydofus2.com.ankamagames.dofus.network.types.game.data.items.effects.ObjectEffect import \
    ObjectEffect
from pydofus2.com.ankamagames.dofus.network.types.game.data.items.effects.ObjectEffectCreature import \
    ObjectEffectCreature
from pydofus2.com.ankamagames.dofus.network.types.game.data.items.effects.ObjectEffectDate import \
    ObjectEffectDate
from pydofus2.com.ankamagames.dofus.network.types.game.data.items.effects.ObjectEffectDice import \
    ObjectEffectDice
from pydofus2.com.ankamagames.dofus.network.types.game.data.items.effects.ObjectEffectDuration import \
    ObjectEffectDuration
from pydofus2.com.ankamagames.dofus.network.types.game.data.items.effects.ObjectEffectInteger import \
    ObjectEffectInteger
from pydofus2.com.ankamagames.dofus.network.types.game.data.items.effects.ObjectEffectLadder import \
    ObjectEffectLadder
from pydofus2.com.ankamagames.dofus.network.types.game.data.items.effects.ObjectEffectMinMax import \
    ObjectEffectMinMax
from pydofus2.com.ankamagames.dofus.network.types.game.data.items.effects.ObjectEffectMount import \
    ObjectEffectMount
from pydofus2.com.ankamagames.dofus.network.types.game.data.items.effects.ObjectEffectString import \
    ObjectEffectString


class ObjectEffectAdapter:
    def __init__(self):
        super().__init__()

    @classmethod
    def fromNetwork(cls, oe: ObjectEffect) -> EffectInstance:
        if isinstance(oe, ObjectEffectDice) and oe.actionId == ActionIds.ACTION_INCARNATION:
            effect = EffectInstanceDate()
            effect.year = oe.diceNum
            effect.month = oe.diceSide * 32768 + oe.diceConst
            level = 1
            while True:
                incLevel = IncarnationLevel.getIncarnationLevelByIdAndLevel(oe.diceNum, level)
                if incLevel:
                    incLevel.requiredXp
                level += 1
                incLevelPlusOne = IncarnationLevel.getIncarnationLevelByIdAndLevel(oe.diceNum, level)
                if incLevelPlusOne:
                    nextFloor = incLevelPlusOne.requiredXp
                if nextFloor < effect.month and level < 51:
                    break
                level -= 1
            effect.day = level
            effect.hour = 0
            effect.minute = 0
        else:
            if isinstance(oe, ObjectEffectString):
                effect = EffectInstanceString()
                effect.text = oe.value
            elif isinstance(oe, ObjectEffectInteger):
                effect = EffectInstanceInteger()
                effect.value = oe.value
            elif isinstance(oe, ObjectEffectMinMax):
                effect = EffectInstanceMinMax()
                effect.min = oe.min
                effect.max = oe.max
            elif isinstance(oe, ObjectEffectDice):
                effect = EffectInstanceDice()
                effect.diceNum = oe.diceNum
                effect.diceSide = oe.diceSide
                effect.value = oe.diceConst
            elif isinstance(oe, ObjectEffectDate):
                effect = EffectInstanceDate()
                effect.year = oe.year
                effect.month = oe.month + 1
                effect.day = oe.day
                effect.hour = oe.hour
                effect.minute = oe.minute
            elif isinstance(oe, ObjectEffectDuration):
                effect = EffectInstanceDuration()
                effect.days = oe.days
                effect.hours = oe.hours
                effect.minutes = oe.minutes
            elif isinstance(oe, ObjectEffectLadder):
                effect = EffectInstanceLadder()
                effect.monsterFamilyId = oe.monsterFamilyId
                effect.monsterCount = oe.monsterCount
            elif isinstance(oe, ObjectEffectCreature):
                effect = EffectInstanceCreature()
                effect.monsterFamilyId = oe.monsterFamilyId
            elif isinstance(oe, ObjectEffectMount):
                effect = EffectInstanceMount()
                effect.id = oe.id
                effect.expirationDate = oe.expirationDate
                effect.model = oe.model
                effect.owner = oe.owner
                effect.name = oe.name
                effect.level = oe.level
                effect.sex = oe.sex
                effect.isRideable = oe.isRideable
                effect.isFecondationReady = oe.isFecondationReady
                effect.isFeconded = oe.isFeconded
                effect.reproductionCount = oe.reproductionCount
                effect.reproductionCountMax = oe.reproductionCountMax
                clientEffects = list[EffectInstanceInteger]()
                for serverEffect in oe.effects:
                    intEffect = EffectInstanceInteger()
                    intEffect.value = serverEffect.value
                    intEffect.effectId = serverEffect.actionId
                    intEffect.duration = 0
                    clientEffects.append(intEffect)
                effect.effects = clientEffects
                effect.capacities = oe.capacities
            else:
                effect = EffectInstance()
        effect.effectId = oe.actionId
        effect.duration = 0
        return effect
