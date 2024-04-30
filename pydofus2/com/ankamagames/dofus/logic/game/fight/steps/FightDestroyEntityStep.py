from pydofus2.com.ankamagames.atouin.types.sequences.DestroyEntityStep import DestroyEntityStep
from pydofus2.com.ankamagames.dofus.logic.game.fight.miscs.FightEntitiesHolder import FightEntitiesHolder
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import IFightStep
from pydofus2.com.ankamagames.jerakine.entities.interfaces.IEntity import IEntity


class FightDestroyEntityStep(DestroyEntityStep, IFightStep):
    def __init__(self, entity: IEntity, waitAnim: bool = False, waitAnimForCallback: bool = False):
        super().__init__(entity, waitAnim, waitAnimForCallback)
        FightEntitiesHolder().unholdEntity(entity.id)

    @property
    def stepType(self) -> str:
        return "destroyEntity"

    @property
    def targets(self) -> list[float]:
        return [self._entity.id]
