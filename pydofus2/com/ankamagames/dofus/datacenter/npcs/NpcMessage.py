from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class NpcMessage(IDataCenter):

    MODULE: str = "NpcMessages"

    id: int

    messageId: int

    messageParams: list[str]

    _messageText: str

    def __init__(self):
        super().__init__()

    @classmethod
    def getNpcMessageById(cls, id: int) -> "NpcMessage":
        return GameData().getObject(cls.MODULE, id)

    @property
    def message(self) -> str:
        if not self._messageText:
            self._messageText = I18n.getText(self.messageId)
        return self._messageText

    idAccessors: IdAccessors = IdAccessors(getNpcMessageById, None)
