from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.DofusEntities import DofusEntities
from pydofus2.com.ankamagames.dofus.logic.game.fight.fightEvents.FightEventsHelper import (
    FightEventsHelper,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightEntitiesFrame import (
    FightEntitiesFrame,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.frames.FightSpellCastFrame import (
    FightSpellCastFrame,
)
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import IFightStep
from pydofus2.com.ankamagames.dofus.logic.game.fight.types.FightEventEnum import FightEventEnum
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterInformations import (
    GameFightFighterInformations,
)
from pydofus2.com.ankamagames.dofus.types.entities.AnimatedCharacter import AnimatedCharacter
from pydofus2.com.ankamagames.jerakine.entities.interfaces.IEntity import IEntity
from pydofus2.com.ankamagames.jerakine.entities.interfaces.IMovable import IMovable
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.sequencer.AbstractSequencable import AbstractSequencable
from pydofus2.com.ankamagames.jerakine.sequencer.ISequencer import ISequencer
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint

logger = Logger("Dofus2")


class FightCarryCharacterStep(AbstractSequencable, IFightStep):

    CARRIED_SUBENTITY_CATEGORY: int = 3

    CARRIED_SUBENTITY_INDEX: int = 0

    _fighterId: float

    _carriedId: float

    _cellId: int

    _carrySubSequence: ISequencer

    _noAnimation: bool

    _isCreature: bool

    def __init__(
        self,
        fighterId: float,
        carriedId: float,
        cellId: int = -1,
        noAnimation: bool = False,
    ):
        super().__init__()
        self._fighterId = fighterId
        self._carriedId = carriedId
        self._cellId = cellId
        self._noAnimation = noAnimation
        self._isCreature = Kernel().worker.getFrame("FightEntitiesFrame")

    @property
    def stepType(self) -> str:
        return "carryCharacter"

    def start(self) -> None:
        targetPosition: MapPoint = None
        carriedEntityDirection: int = 0
        entitiesFrame: FightEntitiesFrame = None
        carriedAC: AnimatedCharacter = None
        carriedEntityInfos: GameFightFighterInformations = None
        cEntity: IEntity = DofusEntities.getEntity(self._fighterId)
        position: MapPoint = cEntity.position
        carryingEntity = cEntity
        carriedEntity: IEntity = DofusEntities.getEntity(self._carriedId)
        if not carryingEntity or not carriedEntity:
            logger.warn(
                "Unable to make "
                + self._fighterId
                + " carry "
                + self._carriedId
                + ", one of them is not in the stage."
            )
            self.carryFinished()
            return
        if self._cellId == -1:
            targetPosition = carriedEntity.position
        else:
            targetPosition = MapPoint.fromCellId(self._cellId)
        if targetPosition:
            carriedEntityDirection = position.advancedOrientationTo(targetPosition)
            self.updateCarriedEntityPosition(carryingEntity, carriedEntity)
            entitiesFrame = Kernel().worker.getFrame("FightEntitiesFrame")
            carriedAC = carriedEntity
            while carriedAC:
                carriedEntityInfos = entitiesFrame.getEntityInfos(carriedAC.id)
                if carriedEntityInfos:
                    carriedEntityInfos.disposition.cellId = carriedAC.position.cellId
                    carriedEntityInfos.disposition.direction = carriedEntityDirection
                carriedAC = carriedAC.carriedEntity
        self.carryFinished()

    @property
    def targets(self) -> list[float]:
        return [self._carriedId]

    def updateCarriedEntityPosition(self, pCarryingEntity: IMovable, pCarriedEntity: IMovable) -> None:
        carried: AnimatedCharacter = None
        if not pCarryingEntity and DofusEntities.getEntity(self._fighterId):
            pCarryingEntity = DofusEntities.getEntity(self._fighterId)
        if pCarryingEntity and pCarriedEntity:
            pCarriedEntity.position.cellId = pCarryingEntity.position.cellId
            carried = pCarriedEntity
            if carried.carriedEntity:
                self.updateCarriedEntityPosition(pCarryingEntity, carried.carriedEntity)

    def carryFinished(self, e=None) -> None:
        carrierAnimatedEntity: AnimatedCharacter = None
        carriedAnimatedEntity: AnimatedCharacter = None
        carriedEntity: IEntity = DofusEntities.getEntity(self._carriedId)
        carryingEntity = DofusEntities.getEntity(self._fighterId)
        FightEventsHelper().sendFightEvent(
            FightEventEnum.FIGHTER_CARRY,
            [self._fighterId, self._carriedId],
            0,
            self.castingSpellId,
        )
        FightSpellCastFrame.updateRangeAndTarget()
        fightEntitiesFrame: FightEntitiesFrame = Kernel().worker.getFrame("FightEntitiesFrame")
        if fightEntitiesFrame is not None:
            carrierAnimatedEntity = carryingEntity
            carriedAnimatedEntity = carriedEntity
            if carrierAnimatedEntity is not None and carriedAnimatedEntity is not None:
                fightEntitiesFrame.addCarrier(carrierAnimatedEntity, carriedAnimatedEntity, True)
        self.executeCallbacks()

    def restart(self, pEvt=None) -> None:
        self.start()
