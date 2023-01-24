from pydofus2.com.ankamagames.dofus.internalDatacenter.spells.SpellWrapper import SpellWrapper
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import IFightStep
from pydofus2.com.ankamagames.dofus.logic.game.common.frames.SpellInventoryManagementFrame import (
    SpellInventoryManagementFrame,
)
from pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager import (
    PlayedCharacterManager,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightEntitiesFrame import (
    FightEntitiesFrame,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.CurrentPlayedFighterManager import (
    CurrentPlayedFighterManager,
)
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import AbstractSequencable


class FightSpellCooldownVariationStep(AbstractSequencable, IFightStep):

    _fighterId: float

    _spellId: int

    _actionId: int

    _value: int

    _isGlobal: bool

    def __init__(
        self,
        fighterId: float,
        actionId: int,
        spellId: int,
        value: int,
        isGlobal: bool = False,
    ):
        super().__init__()
        self._fighterId = fighterId
        self._spellId = spellId
        self._actionId = actionId
        self._value = value
        self._isGlobal = isGlobal

    @property
    def stepType(self) -> str:
        return "spellCooldownVariation"

    def start(self) -> None:
        if (
            self._fighterId == CurrentPlayedFighterManager().currentFighterId
            or self._fighterId == PlayedCharacterManager().id
        ):
            spellCastManager = CurrentPlayedFighterManager().getSpellCastManagerById(
                self._fighterId
            )
            simf: "SpellInventoryManagementFrame" = (
                Kernel().worker.getFrame("SpellInventoryManagementFrame")
            )
            spellList = simf.getFullSpellListByOwnerId(self._fighterId)
            for spellKnown in spellList:
                if spellKnown.id == self._spellId:
                    spellLvl = spellKnown.spellLevel
            if spellCastManager and spellLvl > 0:
                if not spellCastManager.getSpellManagerBySpellId(self._spellId):
                    spellCastManager.castSpell(self._spellId, spellLvl, [], False)
                spellManager = spellCastManager.getSpellManagerBySpellId(self._spellId)
                spellManager.forceCooldown(self._value, True)
        if self._isGlobal:
            fightEntitiesFrame = FightEntitiesFrame.getCurrentInstance()
            if fightEntitiesFrame is not None:
                entityIds = fightEntitiesFrame.getEntityIdsWithTeamId(
                    fightEntitiesFrame.getEntityTeamId(self._fighterId)
                )
                spellWrapper = None
                for entityId in entityIds:
                    if self._fighterId == entityId:
                        spellCastManager = (
                            CurrentPlayedFighterManager().getSpellCastManagerById(
                                entityId
                            )
                        )
                        if spellCastManager is not None:
                            spellWrapper = SpellWrapper.getSpellWrapperById(
                                self._spellId, entityId
                            )
                            if spellWrapper is not None:
                                spellManager = (
                                    spellCastManager.getSpellManagerBySpellId(
                                        self._spellId, True, spellWrapper.spellLevel
                                    )
                                )
                                spellManager.forceCooldown(self._value)
        self.executeCallbacks()

    @property
    def targets(self) -> list[float]:
        return [self._fighterId]
