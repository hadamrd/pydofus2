from pydofus2.com.ankamagames.jerakine.messages.QueueableMessage import QueueableMessage
from pydofus2.com.ankamagames.jerakine.network.CustomDataWrapper import ByteArray
from pydofus2.com.ankamagames.jerakine.network.IdentifiedMessage import IdentifiedMessage


class INetworkMessage(IdentifiedMessage, QueueableMessage):
    def pack(self, param1: ByteArray) -> None:
        raise NotImplementedError("This method must be overriden")

    def unpack(self, param1: ByteArray, param2: int) -> None:
        raise NotImplementedError("This method must be overriden")

    @property
    def isInitialized(self) -> bool:
        raise NotImplementedError("This method must be overriden")

    @property
    def unpacked(self) -> bool:
        raise NotImplementedError("This method must be overriden")

    @unpacked.setter
    def unpacked(self, param1: bool) -> None:
        raise NotImplementedError("This method must be overriden")
