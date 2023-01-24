from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.DofusEntities import DofusEntities
from pydofus2.com.ankamagames.dofus.logic.game.fight.actions.RemoveEntityAction import (
    RemoveEntityAction,
)

from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightEntitiesFrame import (
    FightEntitiesFrame,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.miscs.FightEntitiesHolder import (
    FightEntitiesHolder,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import IFightStep
from pydofus2.com.ankamagames.dofus.network.enums.GameActionFightInvisibilityStateEnum import (
    GameActionFightInvisibilityStateEnum,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterInformations import (
    GameFightFighterInformations,
)
from pydofus2.com.ankamagames.dofus.types.entities.AnimatedCharacter import AnimatedCharacter
from pydofus2.com.ankamagames.jerakine.entities.interfaces.IDisplayable import IDisplayable
from pydofus2.com.ankamagames.jerakine.entities.interfaces.IEntity import IEntity
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import AbstractSequencable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightContextFrame import (
        FightContextFrame,
    )


class FightChangeVisibilityStep(AbstractSequencable, IFightStep):

    _entityId: float

    _visibilityState: int

    _oldVisibilityState: int

    def __init__(self, entityId: float, visibilityState: int):
        super().__init__()
        fighterInfos: GameFightFighterInformations = FightEntitiesFrame.getCurrentInstance().getEntityInfos(entityId)
        self._oldVisibilityState = fighterInfos.stats.invisibilityState
        self._entityId = entityId
        self._visibilityState = visibilityState

    @property
    def stepType(self) -> str:
        return "changeVisibility"

    def start(self) -> None:
        if self._visibilityState == GameActionFightInvisibilityStateEnum.VISIBLE:
            invisibleEntity = self.respawnEntity()
            invisibleEntity.alpha = 1

            if isinstance(invisibleEntity, AnimatedCharacter):
                invisibleEntityPos = invisibleEntity.position
                entitiesFrame: FightEntitiesFrame = Kernel().worker.getFrame('FightEntitiesFrame')
                fightEntities = entitiesFrame.entities
                for entityId in fightEntities:
                    entityInfos = entitiesFrame.getEntityInfos(entityId)
                    if (
                        entitiesFrame.entityIsIllusion(entityId)
                        and entityInfos.stats.summoner == self._entityId
                        and entityInfos.disposition.cellId == invisibleEntityPos.cellId
                    ):
                        rea = RemoveEntityAction.create(entityId)
                        entitiesFrame.process(rea)

            if isinstance(invisibleEntity, AnimatedCharacter):
                invisibleEntity.canSeeThrough = False
                invisibleEntity.canWalkThrough = False
                invisibleEntity.canWalkTo = False

        elif self._visibilityState == GameActionFightInvisibilityStateEnum.DETECTED:
            invisibleEntity = self.respawnEntity()

            if isinstance(invisibleEntity, AnimatedCharacter):
                invisibleEntity.canSeeThrough = True
                invisibleEntity.canWalkThrough = False
                invisibleEntity.canWalkTo = False
            invisibleEntity.alpha = 0.5

        elif self._visibilityState == GameActionFightInvisibilityStateEnum.INVISIBLE:
            self.unspawnEntity()

        fcf: "FightContextFrame" = Kernel().worker.getFrame("FightContextFrame")
        if self._visibilityState == GameActionFightInvisibilityStateEnum.INVISIBLE:
            fcf.addToHiddenEntities(self._entityId)
        else:
            fcf.removeFromHiddenEntities(self._entityId)
        fighterInfos: GameFightFighterInformations = FightEntitiesFrame.getCurrentInstance().getEntityInfos(
            self._entityId
        )
        fighterInfos.stats.invisibilityState = self._visibilityState
        self.executeCallbacks()

    @property
    def targets(self) -> list[float]:
        return [self._entityId]

    def unspawnEntity(self) -> None:
        if FightEntitiesHolder().getEntity(self._entityId):
            return
        entity: IDisplayable = DofusEntities.getEntity(self._entityId)
        FightEntitiesHolder().holdEntity(entity)

    def respawnEntity(self) -> IEntity:
        tiphonSprite = DofusEntities().getEntity(self._entityId)
        if tiphonSprite and tiphonSprite.parentSprite:
            fightEntitiesFrame: "FightEntitiesFrame" = Kernel().worker.getFrame("FightEntitiesFrame")
            if fightEntitiesFrame:
                fightEntitiesFrame.addOrUpdateActor(fightEntitiesFrame.getEntityInfos(self._entityId))
            return tiphonSprite
        if FightEntitiesHolder().getEntity(self._entityId):
            FightEntitiesHolder().unholdEntity(self._entityId)
        return DofusEntities.getEntity(self._entityId)
