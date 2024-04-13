import sys

from pydofus2.com.ankamagames.dofus.datacenter.items.EvolutiveItemType import EvolutiveItemType
from pydofus2.com.ankamagames.dofus.datacenter.items.ItemSuperType import ItemSuperType
from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger


class ItemType(IDataCenter):

    MODULE: str = "ItemTypes"

    _zoneSize: int = 4.294967295e9

    _zoneShape: int = 4.294967295e9

    _zoneMinSize: int = 4.294967295e9

    id: int

    nameId: int

    superTypeId: int

    categoryId: int

    isInEncyclopedia: bool

    plural: bool

    gender: int

    rawZone: str

    mimickable: bool

    craftXpRatio: int

    evolutiveTypeId: int

    possiblePositions: list[int] = None

    _name: str = None

    _evolutiveType: EvolutiveItemType = None

    _superType: ItemSuperType = None

    def __init__(self):
        super().__init__()

    @classmethod
    def getItemTypeById(cls, id: int) -> "ItemType":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getItemTypes(cls) -> list:
        return GameData().getObjects(cls.MODULE)

    idAccessors: IdAccessors = IdAccessors(getItemTypeById, getItemTypes)

    @property
    def name(self) -> str:
        if not self._name:
            self._name = I18n.getText(self.nameId)
        return self._name

    @property
    def evolutiveType(self) -> EvolutiveItemType:
        if not self._evolutiveType:
            if self.evolutiveTypeId == 0:
                return None
            self._evolutiveType = EvolutiveItemType.getEvolutiveItemTypeById(self.evolutiveTypeId)
        return self._evolutiveType

    @property
    def zoneSize(self) -> int:
        if self._zoneSize == -sys.maxsize - 1:
            self.parseZone()
        return self._zoneSize

    @property
    def zoneShape(self) -> int:
        if self._zoneShape == -sys.maxsize - 1:
            self.parseZone()
        return self._zoneShape

    @property
    def zoneMinSize(self) -> int:
        if self._zoneMinSize == -sys.maxsize - 1:
            self.parseZone()
        return self._zoneMinSize

    @property
    def superType(self) -> ItemSuperType:
        if self._superType is None:
            self._superType = ItemSuperType.getItemSuperTypeById(self.superTypeId)
        return self._superType

    def parseZone(self) -> None:
        params: list = None
        if self.rawZone and len(self.rawZone):
            self._zoneShape = self.rawZone[0]
            params = self.rawZone[1:].split(",")
            if len(params) > 0:
                self._zoneSize = int(params[0])
            else:
                self._zoneSize = 0
            if len(params) > 1:
                self._zoneMinSize = int(params[1])
            else:
                self._zoneMinSize = 0
        else:
            Logger().error("Zone incorrect (" + self.rawZone + ")")
