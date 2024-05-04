from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.tiphon.types.look.TiphonEntityLook import TiphonEntityLook


class EntityLookObserver:
    def boneChanged(self, param1: "TiphonEntityLook"):
        ...

    def skinsChanged(self, param1: "TiphonEntityLook"):
        ...

    def colorsChanged(self, param1: "TiphonEntityLook"):
        ...

    def scalesChanged(self, param1: "TiphonEntityLook"):
        ...

    def subEntitiesChanged(self, param1: "TiphonEntityLook"):
        ...
