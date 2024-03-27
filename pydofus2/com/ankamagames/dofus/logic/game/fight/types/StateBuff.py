from pydofus2.com.ankamagames.dofus.datacenter.spells.SpellState import \
    SpellState
from pydofus2.com.ankamagames.dofus.internalDatacenter.spells.SpellWrapper import \
    SpellWrapper
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.FightersStateManager import \
    FightersStateManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.miscs.ActionIdHelper import \
    ActionIdHelper
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.BasicBuff import \
    BasicBuff
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.SpellCastSequenceContext import SpellCastSequenceContext
from pydofus2.com.ankamagames.dofus.network.types.game.actions.fight.FightTemporaryBoostStateEffect import \
    FightTemporaryBoostStateEffect


class StateBuff(BasicBuff):
    _statName: str

    _isSilent: bool = True

    _isDisplayTurnRemaining: bool = False

    _isVisibleInFightLog: bool = False

    stateId: int = None

    delta: int

    def __init__(
        self,
        effect: FightTemporaryBoostStateEffect = None,
        castingSpell: SpellCastSequenceContext = None,
        actionId: int = 0,
    ):
        spellState: SpellState = None
        if effect:
            spellState = SpellState.getSpellStateById(effect.stateId)
            super().__init__(effect, castingSpell, actionId, None, None, effect.stateId)
            self._statName = ActionIdHelper.getActionIdStatName(actionId)
            self.stateId = effect.stateId
            self.delta = effect.delta
            self._isSilent = spellState.isSilent
            self._isDisplayTurnRemaining = spellState.displayTurnRemaining
            self._isVisibleInFightLog = self.effect.visibleInFightLog

    @property
    def type(self) -> str:
        return "StateBuff"

    @property
    def statName(self) -> str:
        return self._statName

    @property
    def isSilent(self) -> bool:
        return self._isSilent

    @property
    def isDisplayTurnRemaining(self) -> bool:
        return self._isDisplayTurnRemaining

    @property
    def isVisibleInFightLog(self) -> bool:
        return self._isVisibleInFightLog

    def onApplied(self) -> None:
        self.addBuffState()
        SpellWrapper.refreshAllPlayerSpellHolder(self.targetId)
        super().onApplied()

    def onRemoved(self) -> None:
        self.removeBuffState()
        SpellWrapper.refreshAllPlayerSpellHolder(self.targetId)
        super().onRemoved()

    def clone(self, id: int = 0) -> BasicBuff:
        sb: StateBuff = StateBuff()
        sb._statName = self._statName
        sb.stateId = self.stateId
        sb.id = self.uid
        sb.uid = self.uid
        sb.dataUid = self.dataUid
        sb.actionId = self.actionId
        sb.self.targetId = self.targetId
        sb.castingSpell = self.castingSpell
        sb.duration = self.duration
        sb.dispelable = self.dispelable
        sb.source = self.source
        sb.aliveSource = self.aliveSource
        sb.sourceJustReaffected = self.sourceJustReaffected
        sb.parentBoostUid = self.parentBoostUid
        sb.initParam(self.param1, self.param2, self.param3)
        return sb

    def addBuffState(self) -> None:
        FightersStateManager().addStateOnTarget(self.targetId, self.stateId, self.delta)

    def removeBuffState(self) -> None:
        FightersStateManager().removeStateOnTarget(self.targetId, self.stateId, self.delta)
