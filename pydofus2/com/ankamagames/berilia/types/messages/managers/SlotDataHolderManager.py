from pydofus2.com.ankamagames.jerakine.interfaces.ISlotData import ISlotData
from pydofus2.com.ankamagames.jerakine.interfaces.ISlotDataHolder import ISlotDataHolder


class SlotDataHolderManager:

    _weakHolderReference: dict = dict()

    _linkedSlotsData: list[ISlotData] = []

    def __init__(self, linkedSlotData: ISlotData):
        self._weakHolderReference = dict[ISlotDataHolder, bool]()
        super().__init__()
        self._linkedSlotsData = list[ISlotData]()
        self._linkedSlotsData.append(linkedSlotData)

    def setLinkedSlotData(self, slotData: ISlotData) -> None:
        if not self._linkedSlotsData:
            self._linkedSlotsData = list[ISlotData]()
        if slotData not in self._linkedSlotsData:
            self._linkedSlotsData.append(slotData)

    def addHolder(self, h: ISlotDataHolder) -> None:
        self._weakHolderReference[h] = True

    def removeHolder(self, h: ISlotDataHolder) -> None:
        del self._weakHolderReference[h]

    def getHolders(self) -> list:
        return list(self._weakHolderReference.keys())

    @classmethod
    def refreshAll(cls) -> None:
        for h in cls._weakHolderReference:
            for linkedSlotData in cls._linkedSlotsData:
                if h and ISlotDataHolder(h).data == linkedSlotData:
                    h.refresh()
