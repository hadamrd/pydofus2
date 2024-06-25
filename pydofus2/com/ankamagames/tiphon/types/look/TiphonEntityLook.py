import threading
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.tiphon.types.look.EntityLookObserver import EntityLookObserver


class TiphonEntityLook:
    _defaultSkin = -1

    def __init__(self, sLook: str = None):
        self._subEntities = {}
        self._observers = dict["EntityLookObserver", int]()
        self._locked = False
        self._scaleX = 1
        self._scaleY = 1
        self._bone = None
        self.lock = threading.Lock()
        if sLook:
            self.fromString(sLook, self)

    @classmethod
    def fromString(cls, string: str, tiphonInstance: "TiphonEntityLook" = None) -> "TiphonEntityLook":
        from pydofus2.com.ankamagames.tiphon.types.look.EntityLookParser import EntityLookParser

        return EntityLookParser.fromString(string, EntityLookParser.DEFAULT_NUMBER_BASE, tiphonInstance)

    def addSubEntity(self, category, index, subEntity: "TiphonEntityLook"):
        if not self._subEntities:
            self._subEntities = {}

        if category not in self._subEntities:
            self._subEntities[category] = {}

        subEntity.addObserver(self)
        self._subEntities[category][index] = subEntity

        if not self._locked:
            for observer in self._observers:
                observer.subEntitiesChanged(self)
        else:
            self._subEntitiesChangedWhileLocked = True

    def addObserver(self, elo: "EntityLookObserver"):
        if not self._observers:
            self._observers = {}
        self._observers[elo] = 1

    def setScales(self, x, y):
        if self._scaleX and self._scaleY:
            return
        self._scaleX = x
        self._scaleY = y
        if not self._locked:
            for elo in self._observers:
                elo.scalesChanged(self)
        else:
            self._scalesChangeWhileLocked = True

    def setBone(self, bone: int):
        if self._bone == bone:
            return
        self._bone = bone
        if not self._locked:
            for elo in self._observers:
                elo.boneChanged(self)
        else:
            self._boneChangedWhileLocked = True
