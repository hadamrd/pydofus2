from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.DofusEntities import \
    DofusEntities
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import \
    IFightStep
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterInformations import \
    GameFightFighterInformations
from pydofus2.com.ankamagames.dofus.types.entities.AnimatedCharacter import \
    AnimatedCharacter
from pydofus2.com.ankamagames.jerakine.entities.interfaces.IMovable import \
    IMovable
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import \
    AbstractSequencable
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint


class FightTeleportStep(AbstractSequencable, IFightStep):

    _fighterId: float

    _destinationCell: MapPoint

    def __init__(self, fighterId: float, destinationCell: MapPoint):
        super().__init__()
        self._fighterId = fighterId
        self._destinationCell = destinationCell

    @property
    def stepType(self) -> str:
        return "teleport"

    def start(self) -> None:
        entity: IMovable = DofusEntities().getEntity(self._fighterId)
        if entity:
            entity.jump(self._destinationCell)
        else:
            Logger().warn("Unable to teleport unknown entity " + self._fighterId + ".")
        infos: "GameFightFighterInformations" = Kernel().fightEntitiesFrame.getEntityInfos(self._fighterId)
        infos.disposition.cellId = self._destinationCell.cellId
        carryingEntity: AnimatedCharacter = DofusEntities().getEntity(self._fighterId)
        carriedEntity: AnimatedCharacter = carryingEntity.carriedEntity if carryingEntity.carriedEntity else None
        if carriedEntity:
            carriedEntityInfos = Kernel().fightEntitiesFrame.getEntityInfos(carriedEntity.id)
            carriedEntityInfos.disposition.cellId = infos.disposition.cellId
        self.executeCallbacks()

    @property
    def targets(self) -> list[float]:
        return [self._fighterId]
