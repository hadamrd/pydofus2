from functools import reduce

import pydofus2.com.ankamagames.jerakine.network.NetworkMessage as bnm
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.network.CustomDataWrapper import ByteArray
from pydofus2.com.ankamagames.jerakine.network.parser.ProtocolSpec import (
    D2PROTOCOL,
    ClassSpec,
    FieldSpec,
    ProtocolSpec,
)
from pydofus2.com.ankamagames.jerakine.network.parser.TypeEnum import TypeEnum

dataWrite = {
    name: (getattr(ByteArray, "read" + name), getattr(ByteArray, "write" + name)) for name in D2PROTOCOL["primitives"]
}

PY_PRIMITIVES = {int, float, str, bool}


class EncoderError(Exception):
    def __init__(self, message: str, field: str, instance: "bnm.NetworkMessage"):
        self.field = field
        self.instance = instance
        super().__init__(message)


class NetworkMessageEncoder:
    @classmethod
    def encode(cls, inst: "bnm.NetworkMessage", data=None, random_hash=False) -> ByteArray:
        spec = inst.getSpec()
        try:
            return cls._encode(spec, inst, data, random_hash)
        except Exception as exc:
            raise EncoderError(f"Error while encoding {inst.__class__.__name__} : {inst.__dict__}.\n{exc}") from exc

    @classmethod
    def jsonEncode(cls, inst: "bnm.NetworkMessage", random_hash=False) -> dict:
        spec = inst.getSpec()
        return cls._jsonEncode(spec, inst, random_hash)

    @classmethod
    def writePrimitive(cls, spec: FieldSpec, inst: "bnm.NetworkMessage", data: ByteArray):
        try:
            dataWrite[spec.type][1](data, inst)
        except:
            Logger().error(f"Error while encoding primitive field '{spec.type}' of '{inst}'.")
            raise
        return data

    @classmethod
    def _encode(cls, spec, inst: "bnm.NetworkMessage", data=None, random_hash=False) -> ByteArray:
        if data is None:
            data = ByteArray()
        if type(spec) is FieldSpec:
            if spec.isPrimitive():
                try:
                    return cls.writePrimitive(spec, inst, data)
                except Exception as exc:
                    raise EncoderError(
                        f"Error while writing primitive field '{spec}' of instance '{inst.__class__.__name__}'\n{exc}",
                        spec,
                        inst.__class__.__name__,
                    ) from exc
            if spec.dynamicType:
                spec = inst.getSpec()
                data.writeUnsignedShort(spec.protocolId)
            else:
                spec = ProtocolSpec.getClassSpecByName(spec.typename)
        if spec.parent:
            cls._encode(ProtocolSpec.getClassSpecByName(spec.parent), inst, data)
        cls.writeBooleans(spec.boolfields, inst, data)
        for field in spec.fields:
            if field.optional:
                if hasattr(inst, field.name) and getattr(inst, field.name) is not None:
                    data.writeByte(1)
                else:
                    data.writeByte(0)
                    continue
            if field.isVector():
                try:
                    cls.writeArray(field, getattr(inst, field.name), data)
                except Exception as exc:
                    raise EncoderError(
                        f"Error while writing vector '{field}' of instance '{inst.__class__.__name__}'\n{exc}",
                        field,
                        inst.__class__.__name__,
                    ) from exc
            else:
                try:
                    cls._encode(field, getattr(inst, field.name), data)
                except Exception as exc:
                    raise EncoderError(
                        f"Error while writing field '{field}' of instance '{inst.__class__.__name__}'\n{exc}",
                        field,
                        inst.__class__.__name__,
                    ) from exc
        if hasattr(inst, "hash_function"):
            data.write(getattr(inst, "hash_function"))
        return data

    @classmethod
    def writeBooleans(cls, boolfields: list[FieldSpec], inst, data: ByteArray):
        bits = []
        for var in boolfields:
            bits.append(getattr(inst, var.name))
            if len(bits) == 8:
                data.writeByte(reduce(lambda a, b: 2 * a + b, bits[::-1]))
                bits = []
        if bits:
            data.writeByte(reduce(lambda a, b: 2 * a + b, bits[::-1]))

    @classmethod
    def writeArray(cls, var: FieldSpec, inst, data):
        n = len(inst)
        if var.length is not None:
            assert n == var.length, f"Vector length {n} different from spec length {var.length}!"
        if var.lengthTypeId is not None:
            if TypeEnum(var.lengthTypeId) == TypeEnum.OBJECT:
                raise EncoderError("Vector length type cant be an OBJECT!", var.name, inst.__class__.__name__)
            type_primite_name = TypeEnum.getPrimitiveName(TypeEnum(var.lengthTypeId))
            if type_primite_name is None:
                raise EncoderError(
                    f"Unknown primitive type id {var.lengthTypeId}, {TypeEnum(var.lengthTypeId)}!",
                    var.name,
                    inst.__class__.__name__,
                )
            dataWrite[type_primite_name][1](data, n)
        if var.type in D2PROTOCOL["primitives"]:
            for it in inst:
                dataWrite[var.type][1](data, it)
        else:
            for it in inst:
                cls._encode(ProtocolSpec.getClassSpecByName(var.name), it, data)

    @classmethod
    def _jsonEncode(cls, spec: ClassSpec, inst, random_hash=True) -> dict:
        ans = {"__type__": inst.__class__.__name__}
        if spec.parent is not None:
            ans.update(cls._jsonEncode(ProtocolSpec.getClassSpecByName(spec.parent), inst))
        for bfield in spec.boolfields:
            ans[bfield.name] = getattr(inst, bfield.name)
        for field in spec.fields:
            if field.optional and not hasattr(inst, field.name):
                continue
            value = getattr(inst, field.name)
            if type(value) is list:
                if len(value) == 0:
                    ans[field.name] = []
                    continue
                if type(value[0]) in PY_PRIMITIVES:
                    ans[field.name] = value
                else:
                    ans[field.name] = [cls.jsonEncode(it) for it in value]
            elif type(value) in PY_PRIMITIVES:
                ans[field.name] = value
            else:
                ans[field.name] = cls.jsonEncode(value)
        if hasattr(inst, "hash_function"):
            ans["hash_function"] = getattr(inst, "hash_function")
        return ans

    @classmethod
    def decodeFromJson(cls, json: dict) -> "bnm.NetworkMessage":
        classSpec = ProtocolSpec.getClassSpecByName(json["__type__"])
        instance = classSpec.cls()
        bnm.NetworkMessage.__init__(instance)
        for k, v in json.items():
            if k == "__type__":
                continue
            if type(v) is dict:
                setattr(instance, k, cls.decodeFromJson(v))
            elif type(v) is list:
                if len(v) == 0:
                    setattr(instance, k, [])
                    continue
                if type(v[0]) in PY_PRIMITIVES:
                    setattr(instance, k, v)
                else:
                    setattr(instance, k, [cls.decodeFromJson(it) for it in v])
            else:
                setattr(instance, k, v)
        return instance
