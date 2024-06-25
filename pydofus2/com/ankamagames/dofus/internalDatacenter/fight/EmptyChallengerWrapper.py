from pydofus2.com.ankamagames.dofus.internalDatacenter.fight.ChallengeWrapper import ChallengeWrapper
from pydofus2.com.ankamagames.dofus.internalDatacenter.fight.EnumChallengeCategory import EnumChallengeCategory
from pydofus2.com.ankamagames.dofus.network.enums.ChallengeStateEnum import ChallengeStateEnum
from pydofus2.com.ankamagames.jerakine.data.XmlConfig import XmlConfig
from pydofus2.com.ankamagames.jerakine.types.Uri import Uri


class EmptyChallengeWrapper(ChallengeWrapper):
    def __init__(self):
        super().__init__()

    @staticmethod
    def create():
        return EmptyChallengeWrapper()

    @property
    def id(self):
        return float("nan")

    @property
    def state(self):
        return ChallengeStateEnum.CHALLENGE_RUNNING

    @property
    def iconUri(self):
        return Uri(XmlConfig().getEntry("config.gfx.path.challenges") + "10026.png")

    @property
    def description(self):
        return ""

    @property
    def name(self):
        return ""

    @property
    def categoryId(self):
        return EnumChallengeCategory.FIGHT


class ChallengeTargetWrapper:
    def __init__(self):
        self.targetId = 0
        self.targetCell = 0
        self.targetName = ""
        self.targetlevel = 1
        self.attackers = []
