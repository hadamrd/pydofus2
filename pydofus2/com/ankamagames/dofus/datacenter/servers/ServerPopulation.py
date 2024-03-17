from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter


class ServerPopulation(IDataCenter):

    MODULE: str = "ServerPopulations"

    id: int

    nameId: int

    weight: int

    _name: str

    def __init__(self):
        super().__init__()

    @classmethod
    def getServerPopulationById(cls, id: int) -> "ServerPopulation":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getServerPopulations(cls) -> list["ServerPopulation"]:
        return GameData().getObjects(cls.MODULE)

    idAccessors: IdAccessors = IdAccessors(getServerPopulationById, getServerPopulations)

    @property
    def name(self) -> str:
        if not self._name:
            self._name = I18n.getText(self.nameId)
        return self._name
