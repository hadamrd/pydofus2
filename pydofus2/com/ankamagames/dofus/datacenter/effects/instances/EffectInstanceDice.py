from logging import Logger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.datacenter.effects.EffectInstance import EffectInstance

from pydofus2.com.ankamagames.dofus.datacenter.effects.instances.EffectInstanceInteger import EffectInstanceInteger


class EffectInstanceDice(EffectInstanceInteger):
    def __init__(self):
        super().__init__()
        diceNum: int = None
        diceSide: int = None

    def clone(self) -> "EffectInstance":
        o: EffectInstanceDice = EffectInstanceDice()
        o.rawZone = self.rawZone
        o.effectUid = self.effectUid
        o.effectId = self.effectId
        o.order = self.order
        o.duration = self.duration
        o.delay = self.delay
        o.diceNum = self.diceNum
        o.diceSide = self.diceSide
        o.value = self.value
        o.random = self.random
        o.group = self.group
        o.visibleInTooltip = self.visibleInTooltip
        o.visibleInBuffUi = self.visibleInBuffUi
        o.visibleInFightLog = self.visibleInFightLog
        o.visibleOnTerrain = self.visibleOnTerrain
        o.targetId = self.targetId
        o.targetMask = self.targetMask
        o.delay = self.delay
        o.triggers = self.triggers
        o.effectElement = self.effectElement
        o.spellId = self.spellId
        o.forClientOnly = self.forClientOnly
        o.dispellable = self.dispellable
        return o

    @property
    def parameter0(self) -> object:
        return self.diceNum if self.diceNum != 0 else None

    @parameter0.setter
    def parameter0(self, value: int):
        self.diceNum = value

    @property
    def parameter1(self) -> object:
        return self.diceSide if self.diceSide != 0 else None

    @parameter1.setter
    def parameter1(self, value: int):
        self.diceSide = value

    @property
    def parameter2(self) -> object:
        return self.value if self.value != 0 else None

    @parameter2.setter
    def parameter2(self, value: int):
        self.value = value

    def setParameter(self, paramIndex: int, value) -> None:
        if paramIndex == 0:
            self.diceNum = int(value)

        if paramIndex == 1:
            self.diceSide = int(value)

        if paramIndex == 2:
            self.value = int(value)

    def add(self, term) -> "EffectInstance":
        if isinstance(term, EffectInstanceDice):
            if self.diceSide == 0:
                self.diceSide = self.diceNum
            self.diceNum += term.diceNum
            self.diceSide += term.diceSide if term.diceSide != 0 else term.diceNum
            if self.diceNum == self.diceSide:
                self.diceSide = 0
            self.forceDescriptionRefresh()
        elif isinstance(term, EffectInstanceInteger):
            self.diceNum += term.value
            self.diceSide = int(self.diceSide + term.value) if self.diceSide != 0 else int(0)
            self.forceDescriptionRefresh()
        else:
            Logger().error(term + " cannot be added to EffectInstanceDice.")
        return self
