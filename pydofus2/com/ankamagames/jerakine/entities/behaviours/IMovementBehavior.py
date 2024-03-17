from ast import FunctionType

from pydofus2.com.ankamagames.jerakine.entities.interfaces.IMovable import \
    IMovable
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint
from pydofus2.com.ankamagames.jerakine.types.positions.MovementPath import \
    MovementPath


class IMovementBehavior:
    def move(self, param1: IMovable, param2: MovementPath, param3: FunctionType = None) -> None:
        raise NotImplementedError()

    def jump(self, param1: IMovable, param2: MapPoint) -> None:
        raise NotImplementedError()

    def stop(self, param1: IMovable, param2: bool = False) -> None:
        raise NotImplementedError()

    def isMoving(self, param1: IMovable) -> bool:
        raise NotImplementedError()

    def synchroniseSubEntitiesPosition(self, param1: IMovable, param2=None) -> None:
        raise NotImplementedError()
