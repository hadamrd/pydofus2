from pydofus2.com.ankamagames.jerakine.entities.interfaces.IDisplayable import IDisplayable
from pydofus2.com.ankamagames.jerakine.interfaces.IRectangle import IRectangle


class IDisplayBehavior:
    def getAbsoluteBounds(self, param1: IDisplayable) -> IRectangle:
        raise NotImplementedError()

    def display(self, param1: IDisplayable, param2: int = 0) -> None:
        raise NotImplementedError()

    def remove(self, param1: IDisplayable) -> None:
        raise NotImplementedError()
