from pydofus2.com.ankamagames.dofus.datacenter.items.criterion.GroupItemCriterion import \
    GroupItemCriterion
from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter


class Companion(IDataCenter):

    MODULE: str = "Companions"

    id: int

    nameId: int

    look: str

    webDisplay: bool

    descriptionId: int

    startingSpellLevelId: int

    assetId: int

    characteristics: list[int]

    spells: list[int]

    creatureBoneId: int

    visibility: str

    _name: str

    _desc: str

    def __init__(self):
        super().__init__()

    @classmethod
    def getCompanionById(cls, id: int) -> "Companion":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getCompanions(cls) -> list["Companion"]:
        return GameData().getObjects(cls.MODULE)

    idAccessors: IdAccessors = IdAccessors(getCompanionById, getCompanions)

    @property
    def name(self) -> str:
        if not self._name:
            self._name = I18n.getText(self.nameId)
        return self._name

    @property
    def description(self) -> str:
        if not self._desc:
            self._desc = I18n.getText(self.descriptionId)
        return self._desc

    @property
    def visible(self) -> bool:
        if not self.visibility:
            return True
        gic: GroupItemCriterion = GroupItemCriterion(self.visibility)
        return gic.isRespected
