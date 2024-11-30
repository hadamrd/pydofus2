from pydofus2.com.ankamagames.dofus.datacenter.world.SubArea import SubArea
from pydofus2.com.ankamagames.dofus.internalDatacenter.DataEnum import DataEnum
from pydofus2.com.ankamagames.dofus.types.enums.HintPriorityEnum import HintPriorityEnum
from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.data.IPostInit import IPostInit
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class Hint(IDataCenter, IPostInit):

    MODULE: str = "Hints"

    _allHints: list = None

    id: int

    gfx: int

    nameId: int

    mapId: float

    realMapId: float

    x: int

    y: int

    outdoor: bool

    subareaId: int

    worldMapId: int

    level: int

    _categoryId: int = None

    _priority: int = None

    _name: str = None  # type: ignore

    _undiatricalName: str = None

    _subArea: SubArea = None

    _zaapMapIds: list[float] = None

    def __init__(self):
        super().__init__()

    @classmethod
    def getZaapMapIds(cls):
        if cls._zaapMapIds is None:
            cls._zaapMapIds = []
            for hint in Hint.getHints():
                if hint.gfx == DataEnum.ZAAP_GFX:
                    cls._zaapMapIds.append(hint.mapId)
        return cls._zaapMapIds

    @classmethod
    def getHintById(cls, id: int) -> "Hint":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getHints(cls) -> list["Hint"]:
        if not cls._allHints:
            cls._allHints = GameData().getObjects(cls.MODULE)
        return cls._allHints

    @property
    def categoryId(self) -> int:
        return self._categoryId

    @categoryId.setter
    def categoryId(self, value: int) -> None:
        self._categoryId = value
        if self._categoryId == DataEnum.HINT_CATEGORY_TEMPLES:
            self._priority = HintPriorityEnum.TEMPLES
        if self._categoryId == DataEnum.HINT_CATEGORY_BIDHOUSE or self._categoryId == DataEnum.HINT_CATEGORY_MISC:
            self._priority = HintPriorityEnum.MISC
        if self._categoryId == DataEnum.HINT_CATEGORY_CRAFT_HOUSES:
            self._priority = HintPriorityEnum.CRAFT_HOUSES
        if self._categoryId == DataEnum.HINT_CATEGORY_DUNGEONS:
            self._priority = HintPriorityEnum.DUNGEONS
        if self._categoryId == DataEnum.HINT_CATEGORY_TRANSPORTATIONS:
            self._priority = HintPriorityEnum.TRANSPORTS

    @property
    def name(self) -> str:
        if not self._name:
            self._name = I18n.getText(self.nameId).replace(" \\n ", "\n")
        return self._name

    @property
    def undiatricalName(self) -> str:
        if not self._undiatricalName:
            self._undiatricalName = I18n.getUnDiacriticalText(self.nameId).replace(" \\n ", "\n")
        return self._undiatricalName

    @property
    def subArea(self) -> SubArea:
        if not self._subArea:
            self._subArea = SubArea.getSubAreaByMapId(self.mapId)
        return self._subArea

    @property
    def priority(self) -> int:
        return self._priority

    def postInit(self) -> None:
        self.name
        self.undiatricalName

    idAccessors: IdAccessors = IdAccessors(getHintById, getHints)
