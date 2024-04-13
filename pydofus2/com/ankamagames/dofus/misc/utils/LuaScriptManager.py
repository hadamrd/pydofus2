import lupa

from pydofus2.com.ankamagames.dofus.datacenter.misc.LuaFormula import LuaFormula
from pydofus2.com.ankamagames.jerakine.metaclasses.ThreadSharedSingleton import ThreadSharedSingleton


class LuaScriptManager(metaclass=ThreadSharedSingleton):

    def __init__(self):
        self._lua = lupa.LuaRuntime()

    def executeScript(self, luaFunction, params):
        luaGlobals = self._lua.globals()
        if params is not None:
            for key, value in params.items():
                luaGlobals[key] = value
        try:
            luaResult = self._lua.execute(luaFunction)
            return luaResult
        finally:
            if params is not None:
                for key in params:
                    del luaGlobals[key]

    def executeLuaFormula(self, luaFormulaId, params):
        luaFunction = self.getLuaFunctionFromFormulaId(luaFormulaId)
        return self.executeScript(luaFunction, params)

    def getLuaFunctionFromFormulaId(self, luaFormulaId):
        formula = LuaFormula.getLuaFormulaById(luaFormulaId)  # You need to implement this method
        return self.formatScriptToLuaFunction(formula.luaFormula)

    def formatScriptToLuaFunction(self, scriptCode, functionName="main"):
        return f"{scriptCode}\nreturn {functionName}()\n"
