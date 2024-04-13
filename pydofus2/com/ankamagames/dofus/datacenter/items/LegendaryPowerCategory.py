from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class LegendaryPowerCategory(IDataCenter):

    MODULE: str = "LegendaryPowersCategories"

    id: int

    categoryName: str

    categoryOverridable: bool

    categorySpells: list[int]

    def __init__(self):
        super().__init__()

    def getLegendaryPowerCategoryById(cls, id: int) -> "LegendaryPowerCategory":
        return GameData().getObject(cls.MODULE, id)

    def getLegendaryPowersCategories(cls) -> list["LegendaryPowerCategory"]:
        return GameData().getObjects(cls.MODULE)

    idAccessors: IdAccessors = IdAccessors(getLegendaryPowerCategoryById, getLegendaryPowersCategories)
