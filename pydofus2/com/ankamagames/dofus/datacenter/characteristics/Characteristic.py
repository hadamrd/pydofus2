from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter


class Characteristic(IDataCenter):

    MODULE: str = "Characteristics"

    id: int

    keyword: str

    nameId: int

    asset: str

    categoryId: int

    visible: bool

    order: int

    scaleFormulaId: int

    upgradable: bool

    _name: str = None

    def __init__(self):
        super().__init__()

    @classmethod
    def getCharacteristicById(cls, id: int) -> "Characteristic":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getCharacteristics(cls) -> list["Characteristic"]:
        return GameData().getObjects(cls.MODULE)

    idAccessors: IdAccessors = IdAccessors(getCharacteristicById, getCharacteristics)

    @property
    def name(self) -> str:
        if not self._name:
            self._name = I18n.getText(self.nameId)
        return self._name
