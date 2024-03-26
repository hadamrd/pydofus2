from pydofus2.com.ankamagames.dofus.datacenter.world.Hint import Hint
from pydofus2.com.ankamagames.dofus.datacenter.world.SubArea import SubArea
from pydofus2.com.ankamagames.dofus.internalDatacenter.DataEnum import DataEnum
from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter


class Sign(IDataCenter):
    MODULE = "Signs"

    def __init__(self):
        self.id = None
        self.params = None
        self.skillId = None
        self.textKey = None
        self._hintOrSubAreaId = None
        self._signText = None
        self._hint = None
        self._subArea = None

    @classmethod
    def getSignById(cls, id: int) -> "Sign":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getSigns(cls) -> list["Sign"]:
        return GameData().getObjects(cls.MODULE)

    @property
    def signText(self) -> str:
        if not self._signText:
            self._hintOrSubAreaId = int(self.params.split(",")[0])
            if self.skillId == DataEnum.SKILL_SIGN_FREE_TEXT:
                self._signText = I18n.getText(self.textKey)
            elif self.skillId == DataEnum.SKILL_SIGN_HINT:
                self._hint = Hint.getHintById(self._hintOrSubAreaId)
                self._signText = self._hint.name
            elif self.skillId == DataEnum.SKILL_SIGN_SUBAREA:
                self._signText = SubArea.getSubAreaById(self._hintOrSubAreaId).name
        return self._signText

    idAccessors = IdAccessors(getSignById, getSigns)
