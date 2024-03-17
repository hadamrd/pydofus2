from pydofus2.com.ankamagames.dofus.datacenter.challenges.Challenge import \
    Challenge
from pydofus2.com.ankamagames.dofus.internalDatacenter.fight.ChallengeTargetWrapper import \
    ChallengeTargetWrapper
from pydofus2.com.ankamagames.dofus.internalDatacenter.fight.EnumChallengeCategory import \
    EnumChallengeCategory
from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.challenge.ChallengeTargetWithAttackerInformation import \
    ChallengeTargetWithAttackerInformation
from pydofus2.com.ankamagames.jerakine.data.XmlConfig import XmlConfig


class ChallengeWrapper:
    def __init__(self):
        self._challenge: Challenge = None
        self._id = 0
        self._targets = []
        self._xpBonus = 0
        self._dropBonus = 0
        self._state = 0

    @staticmethod
    def create():
        return ChallengeWrapper()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._challenge = Challenge.getChallengeById(id)
        self._id = id

    def setTargetsFromTargetInformation(self, targets: list[ChallengeTargetWithAttackerInformation]):
        self._targets = list[ChallengeTargetWrapper]()
        for target in targets:
            targetWrapper = ChallengeTargetWrapper()
            targetWrapper.targetId = target.targetId
            targetWrapper.targetCell = target.targetCell
            targetWrapper.targetName = self.getFightFrame().getFighterName(target.targetId)
            targetWrapper.targetLevel = self.getFightFrame().getFighterLevel(target.targetId)
            if isinstance(target, ChallengeTargetWithAttackerInformation):
                targetWrapper.attackers = target.attackersIds
            self._targets.append(targetWrapper)

    @property
    def xpBonus(self):
        return self._xpBonus

    @xpBonus.setter
    def xpBonus(self, bonus):
        self._xpBonus = bonus

    @property
    def dropBonus(self):
        return self._dropBonus

    @dropBonus.setter
    def dropBonus(self, bonus):
        self._dropBonus = bonus

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    @property
    def iconUri(self):
        if self._challenge is not None:
            return self._challenge.iconUri
        return None

    @property
    def description(self):
        return self._challenge.description

    @property
    def targets(self) -> list[ChallengeTargetWrapper]:
        return self._targets

    @property
    def name(self):
        return self._challenge.name

    @property
    def categoryId(self):
        return self._challenge.categoryId

    @property
    def fullSizeIconUri(self):
        return self.iconUri

    @property
    def errorIconUri(self):
        return None

    @property
    def backGroundIconUri(self):
        return None

    @property
    def backgroundColor(self):
        if EnumChallengeCategory.isAchievementCategoryId(self.categoryId):
            return XmlConfig().getEntry("colors.challenge.achievement")
        return XmlConfig().getEntry("colors.challenge.challenge")

    @property
    def info1(self):
        return ""

    @property
    def active(self):
        return True

    @property
    def timer(self):
        return 0

    @property
    def startTime(self):
        return 0

    @property
    def endTime(self):
        return 0

    @endTime.setter
    def endTime(self, t):
        pass

    def addHolder(self, h):
        pass

    def removeHolder(self, h):
        pass

    @property
    def boundAchievements(self):
        return self._challenge.boundAchievements

    def getTurnsNumberForCompletion(self):
        if self._challenge is None:
            return float('nan')
        return self._challenge.getTurnsNumberForCompletion()

    def getBoundBossId(self):
        if self._challenge is None:
            return float('nan')
        return self._challenge.getBoundBossId()

    def getTargetMonsterId(self):
        if self._challenge is None:
            return float('nan')
        return self._challenge.getTargetMonsterId()

    def getPlayersNumberType(self):
        if self._challenge is None:
            return float('nan')
        return self._challenge.getPlayersNumberType()

    def getFightFrame(self):
        return Kernel().fightContextFrame
