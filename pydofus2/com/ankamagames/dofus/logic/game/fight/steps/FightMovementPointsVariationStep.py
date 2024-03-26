from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.abstract.AbstractStatContextualStep import \
    AbstractStatContextualStep
from pydofus2.com.ankamagames.dofus.logic.game.fight.steps.IFightStep import \
    IFightStep
from pydofus2.com.ankamagames.dofus.network.enums.GameContextEnum import \
    GameContextEnum


class FightMovementPointsVariationStep(AbstractStatContextualStep, IFightStep):

    COLOR: int = 26112

    BLOCKING: bool = False

    _intValue: int

    _voluntarlyUsed: bool

    _updateCharacteristicManager: bool

    _showChatmessage: bool

    def __init__(
        self,
        entityId: float,
        value: int,
        voluntarlyUsed: bool,
        updateCharacteristicManager: bool = True,
        showChatMessage: bool = True,
    ):
        super().__init__(
            self.COLOR,
            "+" + str(value) if value > 0 else str(value),
            entityId,
            GameContextEnum.FIGHT,
            self.BLOCKING,
        )
        self._showChatmessage = showChatMessage
        self._intValue = value
        self._voluntarlyUsed = voluntarlyUsed
        self._virtual = self._voluntarlyUsed
        self._updateCharacteristicManager = updateCharacteristicManager

    @property
    def stepType(self) -> str:
        return "movementPointsVariation"

    @property
    def value(self) -> int:
        return self._intValue

    def start(self) -> None:
        if self._updateCharacteristicManager:
            Kernel().fightEntitiesFrame.setLastKnownEntityMovementPoint(self._targetId, -self._intValue, True)
        self.executeCallbacks()
