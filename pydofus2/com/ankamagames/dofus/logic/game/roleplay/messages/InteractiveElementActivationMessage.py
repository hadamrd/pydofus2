from pydofus2.com.ankamagames.dofus.network.types.game.interactive.InteractiveElement import \
    InteractiveElement
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint


class InteractiveElementActivationMessage(Message):

    _ie: InteractiveElement

    _position: MapPoint

    _skillInstanceId: int

    _additionalParam: int

    fromStack: bool

    fromAutotrip: bool

    def __init__(
        self,
        ie: InteractiveElement,
        position: MapPoint,
        skillInstanceId: int,
        additionalParam: int = 0,
    ):
        super().__init__()
        self._ie = ie
        self._position = position
        self._skillInstanceId = skillInstanceId
        self._additionalParam = additionalParam

    @property
    def interactiveElement(self) -> InteractiveElement:
        return self._ie

    @property
    def position(self) -> MapPoint:
        return self._position

    @property
    def skillInstanceId(self) -> int:
        return self._skillInstanceId

    @property
    def additionalParam(self) -> int:
        return self._additionalParam
