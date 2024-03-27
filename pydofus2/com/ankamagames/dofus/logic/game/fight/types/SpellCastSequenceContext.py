import threading
from typing import List, Optional

from pydofus2.com.ankamagames.dofus.datacenter.spells.Spell import Spell
from pydofus2.com.ankamagames.dofus.datacenter.spells.SpellLevel import SpellLevel
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint

class SpellCastSequenceContext:
    """
    Translated class from ActionScript to Python, maintaining original naming conventions
    for properties and methods as much as possible.
    """
    
    NO_ID = 0xFFFFFFFF
    idCounter = {}

    def __init__(self, isId: bool = True):
        if isId:
            thname = threading.current_thread().name
            if thname not in SpellCastSequenceContext.idCounter:
                SpellCastSequenceContext.idCounter[thname] = 0
            self.id = SpellCastSequenceContext.idCounter[thname]
            SpellCastSequenceContext.idCounter[thname] += 1
        else:
            self.id = SpellCastSequenceContext.NO_ID
        self.casterId: float = 0.0
        self.targetedCellId: int = -1
        self.weaponId: int = -1
        self.spellData: Optional['Spell'] = None
        self.spellLevelData: Optional['SpellLevel'] = None
        self.direction: int = -1
        self.markId: int = 0
        self.markType: int = 0
        self.isSilentCast: bool = False
        self.isCriticalHit: bool = False
        self.isCriticalFail: bool = False
        self.portalIds: List[int] = []
        self.portalMapPoints: List['MapPoint'] = []
        self.defaultTargetGfxId: int = 0

    def reset():
        thname = threading.current_thread().name
        if thname in SpellCastSequenceContext.idCounter:
            SpellCastSequenceContext.idCounter[thname] = 0