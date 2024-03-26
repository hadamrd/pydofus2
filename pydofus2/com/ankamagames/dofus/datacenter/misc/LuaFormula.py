from typing import List

from pydofus2.com.ankamagames.jerakine.data.GameData import GameData


class LuaFormula:
    MODULE = "LuaFormulas"

    def __init__(self):
        self.id: int
        self.formulaName: str
        self.luaFormula: str

    @classmethod
    def getLuaFormulaById(cls, id: int) -> "LuaFormula":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getLuaFormulas(cls) -> List["LuaFormula"]:
        return GameData().getObjects(cls.MODULE)
