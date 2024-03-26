from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter


class ItemSuperType(IDataCenter):
    MODULE = "ItemSuperTypes"

    def __init__(self):
        self.id = None
        self.possiblePositions = []

    @staticmethod
    def getItemSuperTypeById(id: int) -> "ItemSuperType":
        return GameData().getObject(ItemSuperType.MODULE, id)

    @staticmethod
    def getItemSuperTypes() -> list["ItemSuperType"]:
        return GameData().getObjects(ItemSuperType.MODULE)

    idAccessors = IdAccessors(getItemSuperTypeById, getItemSuperTypes)
