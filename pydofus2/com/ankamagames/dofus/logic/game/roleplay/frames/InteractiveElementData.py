from pydofus2.com.ankamagames.dofus.network.types.game.interactive.InteractiveElement import InteractiveElement
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint


class InteractiveElementData:

    def __init__(self, element: InteractiveElement, position: MapPoint, skillUID: int) -> None:
        self.element = element
        self.position = position
        self.skillUID = skillUID
        self.skillId = None

    def __repr__(self) -> str:
        return f"InteractiveElementData({self.element}, {self.position}, {self.skillUID})"
