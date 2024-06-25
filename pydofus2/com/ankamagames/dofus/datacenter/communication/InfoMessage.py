from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class InfoMessage(IDataCenter):

    MODULE: str = "InfoMessages"

    typeId: int

    messageId: int

    textId: int

    _text: str = None

    def __init__(self):
        super().__init__()

    @classmethod
    def getInfoMessageById(cls, id: int) -> "InfoMessage":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getInfoMessages(cls) -> list["InfoMessage"]:
        return GameData().getObjects(cls.MODULE)

    @property
    def text(self) -> str:
        if not self._text:
            self._text = I18n.getText(self.textId)
        return self._text

    idAccessors: IdAccessors = IdAccessors(getInfoMessageById, getInfoMessages)
