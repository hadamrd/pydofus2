from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.DofusEntities import \
    DofusEntities
from pydofus2.com.ankamagames.dofus.logic.game.fight.miscs.FightEntitiesHolder import \
    FightEntitiesHolder
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import \
    IFightStep
from pydofus2.com.ankamagames.dofus.network.enums.GameActionFightInvisibilityStateEnum import \
    GameActionFightInvisibilityStateEnum
from pydofus2.com.ankamagames.dofus.types.entities.AnimatedCharacter import \
    AnimatedCharacter
from pydofus2.com.ankamagames.jerakine.entities.interfaces.IEntity import \
    IEntity
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import \
    AbstractSequencable


class FightChangeVisibilityStep(AbstractSequencable, IFightStep):

    _entityId: float
    _visibilityState: int
    _oldVisibilityState: int

    def __init__(self, entityId: float, visibilityState: int):
        super().__init__()
        fighterInfos = Kernel().fightEntitiesFrame.getEntityInfos(entityId)
        self._oldVisibilityState = fighterInfos.stats.invisibilityState
        self._entityId = entityId
        self._visibilityState = visibilityState

    @property
    def stepType(self) -> str:
        return "changeVisibility"

    def start(self) -> None:
        if self._visibilityState == GameActionFightInvisibilityStateEnum.VISIBLE:
            invisibleEntity = self.respawnEntity()
            if isinstance(invisibleEntity, AnimatedCharacter):
                invisibleEntityPos = invisibleEntity.position
                entitiesFrame = Kernel().fightEntitiesFrame
                for entityId, entityInfos in entitiesFrame.entities.items():
                    if (
                        entitiesFrame.entityIsIllusion(entityId)
                        and entityInfos.stats.summoner == self._entityId
                        and entityInfos.disposition.cellId == invisibleEntityPos.cellId
                    ):
                        entitiesFrame.removeEntity(entityId)
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
        elif self._visibilityState == GameActionFightInvisibilityStateEnum.INVISIBLE:
            self.unspawnEntity()
        fcf = Kernel().fightContextFrame
        if self._visibilityState == GameActionFightInvisibilityStateEnum.INVISIBLE:
            fcf.addToHiddenEntities(self._entityId)
        else:
            fcf.removeFromHiddenEntities(self._entityId)
        fighterInfos = Kernel().fightEntitiesFrame.getEntityInfos(self._entityId)
        fighterInfos.stats.invisibilityState = self._visibilityState
        self.executeCallbacks()

    @property
    def targets(self) -> list[float]:
        return [self._entityId]
    
    def unspawnEntity(self) -> None:
        if FightEntitiesHolder().getEntity(self._entityId):
            return
        entity: AnimatedCharacter = DofusEntities().getEntity(self._entityId)
        if not entity:
            entity = Kernel().fightEntitiesFrame.entities.get(self._entityId)
            if not entity:
                return Logger().info("Can't hold entity while invisible coz its not found")
        FightEntitiesHolder().holdEntity(entity)
        if entity:
            entity.hide()

    def respawnEntity(self) -> IEntity:
        tiphonSprite = DofusEntities().getEntity(self._entityId)
        if tiphonSprite:
            fightEntitiesFrame = Kernel().fightEntitiesFrame
            if fightEntitiesFrame:
                fightEntitiesFrame.addOrUpdateActor(fightEntitiesFrame.getEntityInfos(self._entityId))
            return tiphonSprite
        holdedEntity:AnimatedCharacter = FightEntitiesHolder().getEntity(self._entityId)
        if holdedEntity:
            holdedEntity.show()
            FightEntitiesHolder().unholdEntity(self._entityId)
        Logger().info(f"Entity ({self._entityId}) respawned.")
        return DofusEntities().getEntity(self._entityId)
