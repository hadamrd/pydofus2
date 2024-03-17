from pydofus2.com.ankamagames.dofus.network.enums.GameActionMarkTypeEnum import \
    GameActionMarkTypeEnum
from pydofus2.com.ankamagames.dofus.types.entities.Projectile import Projectile
from pydofus2.com.ankamagames.jerakine.interfaces.IObstacle import IObstacle


class Glyph(Projectile, IObstacle):

    glyphType: int

    def __init__(
        self,
        nId: int,
        look,
        postInit: bool = False,
        startPlayingOnlyWhenDisplayed: bool = True,
        glyphType: int = 0,
    ):
        super().__init__(nId, look, postInit, startPlayingOnlyWhenDisplayed)
        self.glyphType = glyphType

    def canSeeThrough(self) -> bool:
        return True

    def canWalkThrough(self) -> bool:
        v: bool = True
        if self.glyphType == GameActionMarkTypeEnum.TRAP or self.glyphType == GameActionMarkTypeEnum.PORTAL:
            v = False
        return v

    def canWalkTo(self) -> bool:
        return True

    def addNumber(self, num: int, color=None) -> None:
        pass

    def getIsTransparencyAllowed(self) -> bool:
        return True
