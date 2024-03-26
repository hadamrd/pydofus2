from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.types.enums.Priority import Priority


class BidHouseManagementFrame(Frame):

    def __init__(self) -> None:
        super().__init__()

    @property
    def priority(self) -> int:
        return Priority.NORMAL

    def pushed(self) -> bool:
        return True

    def pulled(self) -> bool:
        return True

    def process(self, msg):
        raise NotImplementedError()
