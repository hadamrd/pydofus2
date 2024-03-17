from typing import Any

from pydofus2.com.ankamagames.jerakine.interfaces.IDragAndDropHandler import \
    IDragAndDropHandler


class ISlotDataHolder(IDragAndDropHandler):
    def refresh(self) -> None:
        pass

    @property
    def data(self) -> Any:
        pass

    @data.setter
    def data(self, param1) -> None:
        pass
