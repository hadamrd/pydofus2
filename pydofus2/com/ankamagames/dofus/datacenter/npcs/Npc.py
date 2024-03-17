from pydofus2.com.ankamagames.dofus.datacenter.npcs.AnimFunNpcData import \
    AnimFunNpcData
from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter


class Npc(IDataCenter):
    MODULE: str = "Npcs"

    id: int

    nameId: int

    dialogMessages: list[list[int]]

    dialogReplies: list[list[int]]

    actions: list[int]

    gender: int

    look: str

    tokenShop: int

    animFunList: list[AnimFunNpcData]

    fastAnimsFun: bool

    tooltipVisible: bool

    _name: str = None

    def __init__(self):
        super().__init__()

    @classmethod
    def getNpcById(cls, id: int) -> "Npc":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getNpcs(cls) -> list["Npc"]:
        return GameData().getObjects(cls.MODULE)

    idAccessors: IdAccessors = IdAccessors(getNpcById, getNpcs)

    @property
    def name(self) -> str:
        if not self._name:
            self._name = I18n.getText(self.nameId)
        return self._name
