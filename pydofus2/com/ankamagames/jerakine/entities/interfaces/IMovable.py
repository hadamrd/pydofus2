from types import FunctionType
from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.jerakine.entities.interfaces.IEntity import IEntity

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint
    from pydofus2.com.ankamagames.jerakine.types.positions.MovementPath import MovementPath


class IMovable(IEntity):

    @property
    def carriedEntity(self) -> "IEntity":
        raise NotImplementedError()

    @property
    def isMoving(self) -> bool:
        raise NotImplementedError()

    def move(
        self,
        movePath: "MovementPath",
        callback: FunctionType = None,
        cellId=None,
    ) -> None:
        raise NotImplementedError()

    def jump(self, cellId: "MapPoint") -> None:
        pass

    def stop(self, param1: bool = False) -> None:
        raise NotImplementedError()
