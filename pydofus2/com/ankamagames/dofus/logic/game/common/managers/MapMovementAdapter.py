from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint
from pydofus2.com.ankamagames.jerakine.types.positions.MovementPath import MovementPath
from pydofus2.com.ankamagames.jerakine.types.positions.PathElement import PathElement


class MapMovementAdapter:

    DEBUG_ADAPTER: bool = False

    def __init__(self):
        super().__init__()

    @classmethod
    def getServerMovement(cls, path: MovementPath) -> list[int]:
        path.compress()
        movement: list[int] = list[int]()
        moveCount: int = 0
        for pe in path.path:
            lastOrientation = pe.orientation
            value = (int(lastOrientation) & 7) << 12 | pe.step.cellId & 4095
            movement.append(value)
            moveCount += 1
        lastValue = (int(lastOrientation) & 7) << 12 | path.end.cellId & 4095
        movement.append(lastValue)
        if cls.DEBUG_ADAPTER:
            movStr = ""
            for movCell in movement:
                movStr += str(movCell & 4095) + " > "
            Logger().debug("Sending path : " + movStr)
        return movement

    @classmethod
    def getClientMovement(cls, path: list[int]) -> MovementPath:
        mp: MovementPath = MovementPath()
        moveCount: int = 0
        previousElement = None
        for movement in path:
            destination = MapPoint.fromCellId(movement & 4095)
            pe = PathElement()
            pe.step = destination
            if moveCount == 0:
                mp.start = destination
            else:
                previousElement.orientation = previousElement.step.orientationTo(pe.step)
            if moveCount == len(path) - 1:
                mp.end = destination
                break
            mp.addPoint(pe)
            previousElement = pe
            moveCount += 1
        mp.fill()
        if cls.DEBUG_ADAPTER:
            movStr = f"Start : {mp.start.cellId} | "
            for movElement in mp.path:
                movStr += str(movElement.step.cellId) + " > "
            Logger().debug(f"Received path : {movStr} | End : {mp.end.cellId}")
        return mp
