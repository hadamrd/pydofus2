from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.jerakine.sequencer.ISequencableListener import ISequencableListener


class ISequencable:
    def start(self) -> None:
        pass

    def addListener(self, param1: "ISequencableListener") -> None:
        pass

    def removeListener(self, param1: "ISequencableListener") -> None:
        pass

    def __str__(self) -> str:
        pass

    def clear(self) -> None:
        pass

    @property
    def timeout(self) -> int:
        pass

    @timeout.setter
    def timeout(self, param1: int) -> None:
        pass

    @property
    def isTimeout(self) -> bool:
        pass

    @property
    def hasDefaultTimeout(self) -> bool:
        pass
