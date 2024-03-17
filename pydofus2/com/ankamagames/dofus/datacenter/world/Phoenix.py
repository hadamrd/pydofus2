from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter


class Phoenix(IDataCenter):

    MODULE: str = "Phoenixes"

    mapId: float

    def __init__(self):
        super().__init__()

    @classmethod
    def getAllPhoenixes(cls) -> list["Phoenix"]:
        return GameData().getObjects(cls.MODULE)

    idAccessors: IdAccessors = IdAccessors(None, getAllPhoenixes)
