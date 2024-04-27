import threading
import zlib
from threading import Thread
from types import FunctionType
from typing import TYPE_CHECKING

import pydofus2.com.ankamagames.jerakine.network.parser.NetworkMessageClassDefinition as nmcd
import pydofus2.com.ankamagames.jerakine.network.parser.NetworkMessageEncoder as nmencoder
from pydofus2.com.ankamagames.jerakine.network.CustomDataWrapper import ByteArray
from pydofus2.com.ankamagames.jerakine.network.INetworkMessage import INetworkMessage
from pydofus2.com.ankamagames.jerakine.network.parser.ProtocolSpec import ClassSpec, ProtocolSpec

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.messages.common.NetworkDataContainerMessage import (
        NetworkDataContainerMessage,
    )


class NetworkMessage(INetworkMessage):

    GLOBAL_INSTANCE_ID = {}
    PACKET_ID_RIGHT_SHIFT: int = 2
    BIT_MASK: int = 3
    HASH_FUNCTION: FunctionType

    def __init__(self):
        self._instance_id = self.getGlobalInstanceId()
        self.receptionTime: int = None
        self.sourceConnection: str = None
        self._name = None
        self._unpacked: bool = False
        self._raw = None
        super().__init__()

    def computeTypeLen(self, length: int) -> int:
        if length > 65535:
            return 3
        if length > 255:
            return 2
        if length > 0:
            return 1
        return 0

    def subComputeStaticHeader(self, msgId: int, typeLen: int) -> int:
        return msgId << self.PACKET_ID_RIGHT_SHIFT | typeLen

    @property
    def unpacked(self) -> bool:
        return self._unpacked

    @unpacked.setter
    def unpacked(self, value: bool) -> None:
        self._unpacked = value

    def getMessageId(self) -> int:
        return ProtocolSpec.getProtocolIdByName(self.__class__.__name__)

    def getSpec(self) -> ClassSpec:
        return ProtocolSpec.getClassSpecByName(self.__class__.__name__)

    @classmethod
    def unpack(cls, data: ByteArray, length: int = None) -> "NetworkMessage":
        if length is None:
            length = data.remaining()
        if cls.__name__ == "NetworkDataContainerMessage":
            return cls.deserializeAs_NetworkDataContainerMessage(data)
        return nmcd.NetworkMessageClassDefinition(cls.__name__, data.read(length)).deserialize()

    def deserializeAs_NetworkDataContainerMessage(input: ByteArray) -> "NetworkDataContainerMessage":
        from pydofus2.com.ankamagames.dofus.network.messages.common.NetworkDataContainerMessage import (
            NetworkDataContainerMessage,
        )

        msg = NetworkDataContainerMessage()
        _contentLen = input.readVarInt()
        tmpBuffer = input.readBytes(0, _contentLen)
        tmpBuffer = zlib.decompress(tmpBuffer)
        msg.content = tmpBuffer
        msg.unpacked = True
        return msg

    def pack(self, from_client=True) -> ByteArray:
        data = nmencoder.NetworkMessageEncoder.encode(self)
        typelen = self.computeTypeLen(len(data))
        header = 4 * self.getMessageId() + typelen
        packed = ByteArray()
        packed.writeUnsignedShort(header)
        if from_client:
            packed.writeUnsignedInt(self._instance_id)
        packed += len(data).to_bytes(typelen, "big")
        packed += data
        return packed

    def to_json(self) -> dict:
        return nmencoder.NetworkMessageEncoder.jsonEncode(self)

    @classmethod
    def from_json(cls, mjson: dict):
        return nmencoder.NetworkMessageEncoder.decodeFromJson(mjson)

    def __eq__(self, __o: "NetworkMessage") -> bool:
        if __o is None:
            return False
        return self._instance_id == __o._instance_id

    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)

    def __hash__(self) -> int:
        return self._instance_id

    def __str__(self) -> str:
        className = self.__class__.__name__
        return className.split(".")[-1] + " @" + str(self._instance_id)

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def getGlobalInstanceId(cls) -> int:
        threadName = threading.currentThread().getName()
        if threadName not in NetworkMessage.GLOBAL_INSTANCE_ID:
            NetworkMessage.GLOBAL_INSTANCE_ID[threadName] = 0
        NetworkMessage.GLOBAL_INSTANCE_ID[threadName] += 1
        return NetworkMessage.GLOBAL_INSTANCE_ID[threadName]

    @classmethod
    def clearGlobalInstanceId(cls):
        del NetworkMessage.GLOBAL_INSTANCE_ID[Thread.currentThread().getName()]
