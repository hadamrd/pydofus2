from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class NamingRule(IDataCenter):

    MODULE: str = "NamingRules"

    id: int

    minLength: int

    maxLength: int

    regexp: str

    def __init__(self):
        super().__init__()

    @classmethod
    def getNamingRuleById(cls, id: int) -> "NamingRule":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getNamingRules(cls) -> list["NamingRule"]:
        return GameData().getObjects(cls.MODULE)

    idAccessors: IdAccessors = IdAccessors(getNamingRuleById, getNamingRules)
