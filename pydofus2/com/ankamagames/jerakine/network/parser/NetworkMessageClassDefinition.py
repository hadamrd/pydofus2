import pydofus2.com.ankamagames.jerakine.network.NetworkMessage as bnm
import pydofus2.com.ankamagames.jerakine.network.parser.NetworkMessageDataField as nmdf
from pydofus2.com.ankamagames.jerakine.logger.Logger import TraceLogger
from pydofus2.com.ankamagames.jerakine.network.CustomDataWrapper import \
    ByteArray
from pydofus2.com.ankamagames.jerakine.network.parser.BooleanByteWrapper import \
    boolByteWrapper
from pydofus2.com.ankamagames.jerakine.network.parser.ProtocolSpec import (
    FieldSpec, ProtocolSpec)


class NetworkMessageClassDefinition:
    TRACE = False

    def __init__(self, className: str, raw: ByteArray) -> None:
        classSpec = ProtocolSpec.getClassSpecByName(className)
        self.parent = classSpec.parent
        self.fields = classSpec.fields
        self.boolfields = classSpec.boolfields
        self.cls = classSpec.cls
        self.raw = raw

    def deserialize(self, childInstance: object = None) -> object:
        if childInstance is None:
            inst = self.cls()
        else:
            inst = childInstance

        if self.TRACE:
            TraceLogger().debug(
                "------------------ Deserializing {} STARTED-----------------".format(self.cls.__name__)
            )

        if self.parent is not None:
            if self.TRACE:
                TraceLogger().debug(f"Class has parent {self.parent}")
            inst = NetworkMessageClassDefinition(self.parent, self.raw).deserialize(inst)
            if self.TRACE:
                TraceLogger().debug("End of parent deserialization")
                TraceLogger().debug(f"BytesArray positon: {self.raw.position}")

        try:
            for field, value in self.readBooleans(self.boolfields, self.raw).items():
                if self.TRACE:
                    TraceLogger().debug(f"{field} = {value}")
                setattr(inst, field, value)
        except Exception as e:
            TraceLogger().debug(f"Remaining bytes in raw: {self.raw.remaining()}")
            TraceLogger().error(f"Error while reading boolean fields!")
            raise e

        for field in self.fields:
            attrib = field.name
            if self.TRACE:
                TraceLogger().debug(f"Deserializing field '{attrib}', remaining bytes '{self.raw.remaining()}'.")
            if field.optional:
                isProvided = self.raw.readByte()
                if not isProvided:
                    if self.TRACE:
                        TraceLogger().debug(f"Field '{attrib}' is optional and was not provided.")
                    continue
            try:
                value = nmdf.NetMsgDataField(field, self.raw).deserialize()
            except Exception as e:
                TraceLogger().debug(inst.__class__.__name__)
                TraceLogger().debug(self.fields)
                TraceLogger().error(str(e), exc_info=True)
                raise KeyboardInterrupt
            setattr(inst, attrib, value)
        if self.TRACE:
            TraceLogger().debug(
                "------------------ Deserializing {} ENDED---------------------".format(self.cls.__name__)
            )

        if inst.__class__.__base__ == bnm.NetworkMessage:
            bnm.NetworkMessage.__init__(inst)

        return inst

    @classmethod
    def readBooleans(cls, boolfields: list[FieldSpec], raw: ByteArray):
        ans = {}
        n = len(boolfields)
        if n > 0:
            if cls.TRACE:
                TraceLogger().debug("Reading {} booleans".format(n))
                TraceLogger().debug(f"I need {n // 8} bytes")
                TraceLogger().debug(f"Remaining bytes in raw: {raw.remaining()}")
            if raw.remaining() < n // 8:
                raise Exception("Not enough bytes to read booleans")
            for i, var in enumerate(boolfields):
                if i % 8 == 0:
                    _box: int = raw.readByte()
                value = boolByteWrapper.getFlag(_box, i % 8)
                if cls.TRACE:
                    TraceLogger().debug(f"{var.name} = {value}")
                ans[var.name] = value
        return ans
