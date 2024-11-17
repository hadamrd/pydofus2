from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.atouin.messages.EntityMovementCompleteMessage import EntityMovementCompleteMessage
from pydofus2.com.ankamagames.berilia.managers.KernelEvent import KernelEvent
from pydofus2.com.ankamagames.berilia.managers.KernelEventsManager import KernelEventsManager
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.DofusEntities import DofusEntities
from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.CurrentPlayedFighterManager import (
    CurrentPlayedFighterManager,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameMapMovementMessage import GameMapMovementMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameMapNoMovementMessage import (
    GameMapNoMovementMessage,
)
from pydofus2.com.ankamagames.jerakine.entities.interfaces.IEntity import IEntity
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority

if TYPE_CHECKING:
    pass


class FightTurnFrame(Frame):

    TAKLED_CURSOR_NAME: str = "TackledCursor"

    SELECTION_PATH: str = "FightMovementPath"

    SELECTION_END_PATH: str = "FightMovementEndPath"

    SELECTION_PATH_TACKLED: str = "FightMovementPathTackled"

    SELECTION_PATH_UNREACHABLE: str = "FightMovementPathUnreachable"

    SELECTION_MOVEMENT_AREA: str = "FightMovementArea"

    REMIND_TURN_DELAY: int = 15

    _isRequestingMovement: bool = None

    _myTurn: bool = None

    _playerEntity: IEntity = None

    _currentFighterId: float = None

    def __init__(self):
        super().__init__()

    @property
    def priority(self) -> int:
        return Priority.HIGH

    @property
    def myTurn(self) -> bool:
        return self._myTurn

    @myTurn.setter
    def myTurn(self, b: bool) -> None:
        self._finishingTurn = False
        self._currentFighterId = CurrentPlayedFighterManager().currentFighterId
        self._playerEntity = DofusEntities().getEntity(self._currentFighterId)
        self._myTurn = b
        if not self._myTurn:
            self._isRequestingMovement = False

    @property
    def turnDuration(self) -> int:
        return self._turnDuration

    @turnDuration.setter
    def turnDuration(self, v: int) -> None:
        self._turnDuration = v

    def freePlayer(self) -> None:
        self._isRequestingMovement = False

    def pushed(self) -> bool:
        Logger().info("FightTurnFrame pushed")
        return True

    def process(self, msg: Message) -> bool:

        if isinstance(msg, GameMapNoMovementMessage):
            if self.myTurn:
                self._isRequestingMovement = False
            KernelEventsManager().send(KernelEvent.FightMovementFailed)
            return False

        elif isinstance(msg, EntityMovementCompleteMessage):
            if self.myTurn:
                self._isRequestingMovement = False
            return False

        if isinstance(msg, GameMapMovementMessage):
            self._isRequestingMovement = False
            return True

    def pulled(self) -> bool:
        Logger().info("FightTurnFrame pulled")
        return True
