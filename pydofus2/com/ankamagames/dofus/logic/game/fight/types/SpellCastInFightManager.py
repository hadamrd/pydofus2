from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.castSpellManager.SpellManager import \
    SpellManager

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightSpellCooldown import \
        GameFightSpellCooldown

class SpellCastInFightManager:

    _spells: dict[int, SpellManager]

    _storedSpellCooldowns: list["GameFightSpellCooldown"]

    currentTurn: int = 1

    entityId: float

    needCooldownUpdate: bool = False

    def __init__(self, entityId: float):
        self._spells = dict[int, SpellManager]()
        super().__init__()
        self.entityId = entityId

    def nextTurn(self) -> None:
        self.currentTurn += 1
        for spell in self._spells.values():
            spell.newTurn()

    def resetInitialCooldown(self, hasBeenSummoned: bool = False) -> None:
        spellList = Kernel().spellInventoryManagementFrame.getFullSpellListByOwnerId(self.entityId)
        for spellWrapper in spellList:
            if spellWrapper.spellLevelInfos.initialCooldown != 0:
                if hasBeenSummoned and spellWrapper.actualCooldown > spellWrapper.spellLevelInfos.initialCooldown:
                    return
                if self._spells.get(spellWrapper.spellId) is None:
                    self._spells[spellWrapper.spellId] = SpellManager(
                        self, spellWrapper.spellId, spellWrapper.spellLevel
                    )
                spellManager = self._spells[spellWrapper.spellId]
                spellManager.resetInitialCooldown(self.currentTurn)

    def updateCooldowns(self, spellCooldowns: list["GameFightSpellCooldown"] = None) -> None:
        from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.CurrentPlayedFighterManager import \
            CurrentPlayedFighterManager
        if self.needCooldownUpdate and not spellCooldowns:
            spellCooldowns = self._storedSpellCooldowns
        playedFighterManager = CurrentPlayedFighterManager()
        numCoolDown = len(spellCooldowns)
        for k in range(numCoolDown):
            spellCooldown = spellCooldowns[k]
            from pydofus2.com.ankamagames.dofus.internalDatacenter.spells.SpellWrapper import \
                SpellWrapper

            spellW = SpellWrapper.getSpellWrapperById(spellCooldown.spellId, self.entityId)
            if not spellW:
                self.needCooldownUpdate = True
                self._storedSpellCooldowns = spellCooldowns
                return
            if spellW and spellW.spellLevel > 0:
                spellLevel = spellW.spell.getSpellLevel(spellW.spellLevel)
                spellCastManager = playedFighterManager.getSpellCastManagerById(self.entityId)
                spellCastManager.castSpell(spellW.id, spellW.spellLevel, [], False)
                interval = int(spellLevel.minCastInterval)
                spellCastManager.getSpellManagerBySpellId(spellW.id).forceLastCastTurn(
                    self.currentTurn + spellCooldown.cooldown - interval
                )
        self.needCooldownUpdate = False

    def castSpell(
        self,
        pSpellId: int,
        pSpellLevel: int,
        pTargets: list,
        pCountForCooldown: bool = True,
    ) -> None:
        if self._spells.get(pSpellId) is None:
            self._spells[pSpellId] = SpellManager(self, pSpellId, pSpellLevel)
        self._spells[pSpellId].cast(self.currentTurn, pTargets, pCountForCooldown)

    def getSpellManagerBySpellId(
        self, pSpellId: int, isForceNewInstance: bool = False, pSpellLevelId: int = -1
    ) -> SpellManager:
        spellManager = self._spells.get(pSpellId)
        if spellManager is None and isForceNewInstance and pSpellLevelId != -1:
            spellManager = self._spells[pSpellId] = SpellManager(self, pSpellId, pSpellLevelId)
        return spellManager
