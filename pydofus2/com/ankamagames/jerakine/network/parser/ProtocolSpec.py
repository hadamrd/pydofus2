import importlib
import json
import os

import pydofus2.com.ankamagames.dofus.settings as settings
from pydofus2.com.ankamagames.jerakine.network.INetworkMessage import \
    INetworkMessage
from pydofus2.com.ankamagames.jerakine.network.parser.TypeEnum import TypeEnum

ROOTDIR = os.path.dirname(__file__)
if not os.path.exists(settings.PROTOCOL_SPEC_PATH):
    raise Exception(f"{settings.PROTOCOL_SPEC_PATH} file not found")
with open(settings.PROTOCOL_SPEC_PATH, "r") as fp:
    D2PROTOCOL = json.load(fp)


class ClassSpec:

    def __init__(self, infos: dict) -> None:
        self.parent: str = infos.get("parent")
        self.package: str = infos.get("package")
        self.name: str = infos.get("name")
        self.protocolId: int = infos.get("protocolId")
        self.hash_function: str = infos.get("hash_function")
        self.fields = [FieldSpec(f) for f in infos.get("fields")]
        self.boolfields = [FieldSpec(f) for f in infos.get("boolfields")]
        modulePath = self.package
        try:
            self.clsModule = globals()[modulePath]
        except:
            self.clsModule = importlib.import_module(modulePath)
        self.cls: INetworkMessage = getattr(self.clsModule, self.name)
        self.json = infos

    def __repr__(self) -> str:
        return json.dumps(self.json)


class FieldSpec:

    def __init__(self, infos: dict):
        self.dynamicType: bool = infos.get("dynamicType")
        self.length: int = infos.get("length")
        self.lengthTypeId: int = infos.get("lengthTypeId")
        self.name: str = infos.get("name")
        self.optional: bool = infos.get("optional")
        self.type: str = infos.get("type")
        self.typeId: TypeEnum = TypeEnum(infos.get("typeId"))
        self.typename: str = infos.get("typename")
        self.json = infos

    def isPrimitive(self):
        return self.typeId != TypeEnum.OBJECT

    def isVector(self):
        return self.length or self.lengthTypeId

    def __repr__(self) -> str:
        return json.dumps(self.json)


class ProtocolSpec:

    @staticmethod
    def getTypeSpecById(id):
        if str(id) not in D2PROTOCOL["type_by_id"]:
            raise AttributeError(f"Type id {id} not found in known types ids")
        return ClassSpec(D2PROTOCOL["type_by_id"][str(id)])

    @staticmethod
    def getClassSpecById(id) -> ClassSpec:
        if str(id) not in D2PROTOCOL["msg_by_id"]:
            raise AttributeError(f"msg id {id} not found in known msg ids")
        return ClassSpec(D2PROTOCOL["msg_by_id"][str(id)])

    @staticmethod
    def getClassSpecByName(name) -> ClassSpec:
        if name not in D2PROTOCOL["type"]:
            raise AttributeError(f"msg name {name} not found in known msg types")
        return ClassSpec(D2PROTOCOL["type"][name])

    @classmethod
    def getMsgNameById(cls, id):
        return cls.getClassSpecById(id).name

    @classmethod
    def getProtocolIdByName(cls, name):
        return cls.getClassSpecByName(name).protocolId
