import random

from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import IFightStep
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.SpellCastSequenceContext import SpellCastSequenceContext
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import AbstractSequencable


class FightPlaySpellScriptStep(AbstractSequencable, IFightStep):

    _fighterId: float

    def __init__(self, context: SpellCastSequenceContext):
        super().__init__()
        # self._casterIds = []
        # if not contexts:
        #     return
        # for context in contexts:
        #     self.handleFightContext(context, spellRank, spellCastSequence)

        if not context.spellLevelData or not context.spellLevelData.playAnimation:
            return
        Logger().debug(f"Fighter {context.casterId} Casting Spell '{context.spellData.name}' ({context.spellData.id})")
        Kernel().worker.terminated.wait(0.1 + abs(random.gauss(0, 0.3)))

    # def handleFightContext(self, context: SpellScriptContext, spellRank: int, spellCastSequence: ISpellCastSequence) -> None:
    #     if context.casterId not in self._casterIds:
    #         self._casterIds.append(context.casterId)
    #     spellData = Spell.getSpellById(context.spellId)
    #     spellLevelData = spellData.getSpellLevel(spellRank) if spellData else None
    #     if not spellLevelData or not spellLevelData.playAnimation:
    #         return
    #     Logger().debug(
    #         f"Fighter {context.casterId} Casting Spell '{spellData.name}' ({spellData.id})"
    #     )
    #     Kernel().worker.terminated.wait(0.3 + abs(random.gauss(0, 0.3)))
    # spellScriptManager().run(context, spellCastSequence, Callback(self.scriptEnd,True), Callback(self.scriptEnd,False))

    def start(self) -> None:
        self.executeCallbacks()

    @property
    def stepType(self) -> str:
        return "spellCast"

    @property
    def targets(self) -> list[float]:
        return [self._casterIds]

    def scriptEnd(self, success: bool) -> None:
        if success:
            return
        Logger().error("Spell script failed")
