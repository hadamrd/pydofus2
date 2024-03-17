import importlib
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.jerakine.data.ModuleReader import ModuleReader

from pydofus2.com.ankamagames.jerakine.data.BinaryStream import BinaryStream
from pydofus2.com.ankamagames.jerakine.data.GameDataField import GameDataField
from pydofus2.com.ankamagames.jerakine.data.IPostInit import IPostInit


class GameDataClassDefinition:
    def __init__(self, packageName: str, className: str, moduleReader: "ModuleReader") -> None:
        moduleName = f"pydofus2.{packageName}.{className}"
        try:
            module = globals()[moduleName]
        except:
            module = importlib.import_module(moduleName)
        self._moduleName = moduleName
        self._name = className
        self._class = getattr(module, className)
        self._fields = list[GameDataField]()
        self.moduleReader = moduleReader

    @property
    def fields(self) -> list[GameDataField]:
        return self._fields

    def from_stream(self, stream: BinaryStream) -> Any:
        inst = self._class()
        for field in self._fields:
            attrib = field.name
            value = field.readData(stream)
            setattr(inst, attrib, value)
        if isinstance(inst, IPostInit):
            inst.postInit()
        return inst

    def addField(self, fileName: str, stream: BinaryStream) -> None:
        field = GameDataField(fileName, self.moduleReader)
        field.readType(stream)
        self._fields.append(field)
