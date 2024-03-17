from typing import TYPE_CHECKING

import pydofus2.com.ankamagames.dofus.internalDatacenter.spells.SpellWrapper as spellw
from pydofus2.com.ankamagames.dofus.datacenter.optionalFeatures.ForgettableSpell import \
    ForgettableSpell
from pydofus2.com.ankamagames.dofus.datacenter.spells.Spell import Spell
from pydofus2.com.ankamagames.dofus.datacenter.spells.SpellLevel import \
    SpellLevel
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.SpellModifiersManager import \
    SpellModifiersManager
from pydofus2.com.ankamagames.dofus.network.enums.SpellModifierTypeEnum import \
    SpellModifierTypeEnum

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.logic.game.fight.types.SpellCastInFightManager import \
        SpellCastInFightManager


class SpellManager:

    _spellId: int = 0

    _spellLevel: int = 0

    _lastCastTurn: int = 0

    _spellHasBeenCast: bool = False

    _forcedCooldown: bool = False

    _lastInitialCooldownReset: int = 0

    _castThisTurn: int = 0

    _targetsThisTurn: dict = None

    _spellCastManager: "SpellCastInFightManager" = None

    def __init__(
        self,
        spellCastManager: "SpellCastInFightManager",
        pSpellId: int,
        pSpellLevel: int,
    ):
        super().__init__()
        self._spellCastManager = spellCastManager
        self._spellId = pSpellId
        self._spellLevel = pSpellLevel
        self._targetsThisTurn = dict()

    def isForgettableSpell(self, spellId: int) -> bool:
        return ForgettableSpell.getForgettableSpellById(spellId) is not None

    @property
    def numberCastThisTurn(self) -> int:
        return self._castThisTurn

    @property
    def spellLevel(self) -> int:
        return self._spellLevel

    @spellLevel.setter
    def spellLevel(self, pSpellLevel: int) -> None:
        self._spellLevel = pSpellLevel

    @property
    def spell(self) -> Spell:
        return Spell.getSpellById(self._spellId)

    def cast(self, pTurn: int, pTarget: list, pCountForCooldown: bool = True) -> None:
        self._lastCastTurn = pTurn
        self._forcedCooldown = False
        self._spellHasBeenCast = True
        for target in pTarget:
            if self._targetsThisTurn.get(target) is None:
                self._targetsThisTurn[target] = 0
            self._targetsThisTurn[target] += 1
        if pCountForCooldown:
            self._castThisTurn += 1
        self.updateSpellWrapper()

    def resetInitialCooldown(self, pTurn: int) -> None:
        self._lastInitialCooldownReset = pTurn
        self.updateSpellWrapper()

    def getCastOnEntity(self, pEntityId: float) -> int:
        if self._targetsThisTurn.get(pEntityId) is None:
            return 0
        return self._targetsThisTurn[pEntityId]

    def newTurn(self) -> None:
        self._castThisTurn = 0
        self._targetsThisTurn = dict()
        self.updateSpellWrapper()

    @property
    def cooldown(self) -> float:
        cooldown = 0
        spell = Spell.getSpellById(self._spellId)
        spellLevel = spell.getSpellLevel(self._spellLevel)
        interval = SpellModifiersManager().getModifiedInt(
            self._spellCastManager.entityId,
            self._spellId,
            SpellModifierTypeEnum.CAST_INTERVAL,
            spellLevel.minCastInterval
        )
        if interval == 63:
            return 63
        initialCooldown = (
            self._lastInitialCooldownReset + spellLevel.initialCooldown - self._spellCastManager.currentTurn
        )
        if (
            self._lastCastTurn >= self._lastInitialCooldownReset + spellLevel.initialCooldown
            or spellLevel.initialCooldown == 0
            or self._forcedCooldown
            or self._castThisTurn > 0
            or self._spellHasBeenCast
        ):
            cooldown = interval + self._lastCastTurn - self._spellCastManager.currentTurn
        else:
            cooldown = initialCooldown
        return min(cooldown, 0)

    def forceCooldown(self, cooldown: int, isBonusRefresh: bool = False) -> None:
        spell: Spell = Spell.getSpellById(self._spellId)
        spellL: SpellLevel = spell.getSpellLevel(self._spellLevel)
        self._lastCastTurn = cooldown + self._spellCastManager.currentTurn - spellL.minCastInterval
        self._forcedCooldown = True
        spellW: spellw.SpellWrapper = spellw.SpellWrapper.getSpellWrapperById(
            self._spellId, self._spellCastManager.entityId
        )
        if isBonusRefresh:
            cooldown = SpellModifiersManager().getModifiedInt(self._spellCastManager.entityId, self._spellId, SpellModifierTypeEnum.CAST_INTERVAL, cooldown)
        spellW.actualCooldown = cooldown

    def forceLastCastTurn(self, pLastCastTurn: int) -> None:
        self._lastCastTurn = pLastCastTurn
        self._forcedCooldown = False
        self.updateSpellWrapper()

    def updateSpellWrapper(self) -> None:
        spellW: spellw.SpellWrapper = spellw.SpellWrapper.getSpellWrapperById(
            self._spellId, self._spellCastManager.entityId
        )
        if spellW is None:
            spellW = spellw.SpellWrapper.create(self._spellId, self._spellLevel, True, self._spellCastManager.entityId)
        if spellW and spellW.actualCooldown != 63:
            spellW.actualCooldown = self.cooldown
