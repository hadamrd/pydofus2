from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.context.GameContextActorInformations import (
        GameContextActorInformations,
    )

from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import IFightStep
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import AbstractSequencable


class FightRefreshFighterStep(AbstractSequencable, IFightStep):

    _infos: "GameContextActorInformations"

    def __init__(self, pFighterInfos: "GameContextActorInformations"):
        super().__init__()
        self._infos = pFighterInfos

    @property
    def stepType(self) -> str:
        return "refreshFighter"

    def start(self) -> None:
        fightEntitiesFrame = Kernel().fightEntitiesFrame
        currentFighterInfos: "GameContextActorInformations" = fightEntitiesFrame.getEntityInfos(
            self._infos.contextualId
        )
        if currentFighterInfos:
            currentFighterInfos.disposition = self._infos.disposition
            currentFighterInfos.look = self._infos.look
            fightEntitiesFrame.setRealFighterLook(currentFighterInfos.contextualId, self._infos.look)
            fightEntitiesFrame.updateActor(currentFighterInfos, True)
        self.executeCallbacks()

    @property
    def targets(self) -> list[float]:
        return [self._infos.contextualId]
