from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class SpellScript(IDataCenter):
    INVALID_ID = -1
    WEAPON_SCRIPT_ID = 0
    WEAPON_TYPE_SCRIPT_ID = 7
    FECA_GLYPH_SCRIPT_ID = 16288
    SRAM_TRAP_SCRIPT_ID = 16289
    MODULE = "SpellScripts"

    def __init__(self):
        self._params = {}
        self.id = 0
        self.typeId = 0
        self.rawParams = ""
        self._weaponScriptData = None
        self._fallbackScriptData = None

    @classmethod
    def getSpellScriptById(cls, id) -> "SpellScript":
        if id == cls.WEAPON_SCRIPT_ID:
            if cls._weaponScriptData is None:
                cls._weaponScriptData = SpellScript()
                cls._weaponScriptData.typeId = SpellScript.WEAPON_TYPE_SCRIPT_ID
            return cls._weaponScriptData

        scriptData = GameData().getObject(cls.MODULE, id)
        if scriptData is None:
            if cls._fallbackScriptData is None:
                cls._fallbackScriptData = SpellScript()
                cls._fallbackScriptData.typeId = SpellScript.INVALID_ID
            scriptData = cls._fallbackScriptData
        return scriptData

    @classmethod
    def getSpellScripts(cls) -> list["SpellScript"]:
        return GameData().getObjects(cls.MODULE)

    def hasParam(self, name: str) -> bool:
        value = self.getStringParam(name)
        try:
            return value is not None and not (value == "" or float(value) != float(value))  # NaN check in Python
        except ValueError:
            return False

    def getNumberParam(self, name):
        rawNumber = self.getStringParam(name)
        if not rawNumber:
            return 0
        try:
            number = float(rawNumber)
            return number
        except ValueError:
            return 0

    def getBoolParam(self, name):
        return self.getNumberParam(name) != 0

    def getStringParam(self, name):
        return self.getParam(name)

    def getParam(self, name):
        if not self.rawParams:
            return None
        if self._params:
            return self._params.get(name)
        splitRawParams = self.rawParams.split(",")
        for rawParam in splitRawParams:
            paramPair = rawParam.split(":")
            if len(paramPair) >= 2:
                key, value = paramPair
                self._params[key] = value
        return self._params.get(name)

    def __str__(self):
        return f"SpellScript id: {self.id}, typeId: {self.typeId}"
