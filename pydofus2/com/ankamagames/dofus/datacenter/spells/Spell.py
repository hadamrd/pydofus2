import re
from typing import TYPE_CHECKING, Any

from pydofus2.com.ankamagames.dofus.datacenter.spells.BoundScriptUsageData import BoundScriptUsageData
from pydofus2.com.ankamagames.dofus.datacenter.spells.SpellScript import SpellScript
from pydofus2.com.ankamagames.dofus.datacenter.spells.SpellType import \
    SpellType
from pydofus2.com.ankamagames.dofus.datacenter.spells.SpellVariant import \
    SpellVariant
from pydofus2.com.ankamagames.dofus.types.IdAccessors import IdAccessors
from pydofus2.com.ankamagames.jerakine.data.GameData import GameData
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import \
    IDataCenter

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.datacenter.spells.SpellLevel import SpellLevel
    from pydofus2.com.ankamagames.dofus.datacenter.spells.EffectZone import EffectZone



class Spell(IDataCenter):

    MODULE: str = "Spells"

    def __init__(self):
        super().__init__()
        self.id: int = 0
        self.nameId: int = 0
        self.descriptionId: int = 0
        self.typeId: int = 0
        self.order: int = 0
        self.iconId: int = None
        self.spellLevels = list[int]()
        self.useParamCache: bool = True
        self.verbose_cast: bool = False
        self.default_zone: str = "0"
        self.bypassSummoningLimit: bool = False
        self.canAlwaysTriggerSpells: bool = False
        self.adminName: str = ""
        self._name: str = ""
        self._description: str = ""
        self._spellLevels = list["SpellLevel"]()
        self._spellVariant: SpellVariant = None
        self.boundScriptUsageData: BoundScriptUsageData = None
        self.criticalHitBoundScriptUsageData: BoundScriptUsageData = None
        self.defaultPreviewZone:str = ""
        self._effectZone: "EffectZone" = None
    
    @classmethod
    def getSpellById(cls, id: int) -> "Spell":
        return GameData().getObject(cls.MODULE, id)

    @classmethod
    def getSpells(cls) -> list["Spell"]:
        return GameData().getObjects(cls.MODULE)

    @property
    def effectZone(self) -> "EffectZone":
        from pydofus2.com.ankamagames.dofus.datacenter.spells.EffectZone import EffectZone

        if self._effectZone is None:
            self._effectZone = EffectZone()
            self._effectZone.rawActivationZone = self.defaultPreviewZone
        return self._effectZone
    
    idAccessors: IdAccessors = IdAccessors(getSpellById, getSpells)

    @property
    def name(self) -> str:
        if not self._name:
            self._name = I18n.getText(self.nameId)
        return self._name

    @property
    def description(self) -> str:
        if not self._description:
            self._description = I18n.getText(self.descriptionId)
        return self._description

    @property
    def type(self) -> SpellType:
        return SpellType.getSpellTypeById(self.typeId)

    @property
    def spellVariant(self) -> SpellVariant:
        allSpellVariants: list = None
        variant: SpellVariant = None
        if self._spellVariant is None:
            allSpellVariants = SpellVariant.getSpellVariants()
            for variant in allSpellVariants:
                if self.id in variant.spellIds:
                    self._spellVariant = variant
                    return self._spellVariant
        return self._spellVariant

    def getSpellLevel(self, level: int):
        _ = self.spellLevelsInfo
        index: int = 0
        if len(self.spellLevels) >= level and level > 0:
            index = level - 1
        return self._spellLevels[index]

    @property
    def spellLevelsInfo(self) -> list:
        from pydofus2.com.ankamagames.dofus.datacenter.spells.SpellLevel import \
            SpellLevel

        if self._spellLevels is None or len(self._spellLevels) != len(self.spellLevels):
            self._spellLevels = [SpellLevel.getLevelById(spellLvl) for spellLvl in self.spellLevels]
        return self._spellLevels

    def __str__(self):
        return f"{self.name} ({self.id})"
    
    def getScriptConditions(self, index: int, isCritical: bool):
        resolvedConditions = self.criticalHitBoundScriptUsageData if isCritical else self.boundScriptUsageData
        if index >= len(resolvedConditions):
            return None
        return resolvedConditions[index]

    def getScriptParam(self, scriptIndex: int, name: str, isCritical: bool = False):
        conditions = self.getScriptConditions(scriptIndex, isCritical)
        if conditions is None:
            return None
        script = SpellScript.getSpellScriptById(conditions.scriptId)
        if script is None:
            return None
        return script.getStringParam(name)

    def getScriptTypeId(self, scriptIndex: int, isCritical: bool = False) -> int:
        conditions = self.getScriptConditions(scriptIndex, isCritical)
        if conditions is None:
            return 1 if isCritical else 0
        script = SpellScript.getSpellScriptById(conditions.scriptId) if conditions else None
        if script is None:
            return 1 if isCritical else 0
        return script.typeId