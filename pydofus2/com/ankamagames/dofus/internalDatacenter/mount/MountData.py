from pydofus2.com.ankamagames.dofus.datacenter.mounts.Mount import Mount
from pydofus2.com.ankamagames.dofus.datacenter.mounts.MountBehavior import MountBehavior
from pydofus2.com.ankamagames.dofus.datacenter.mounts.MountFamily import MountFamily
from pydofus2.com.ankamagames.dofus.misc.ObjectEffectAdapter import ObjectEffectAdapter
from pydofus2.com.ankamagames.jerakine.data.I18n import I18n
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class MountData(IDataCenter):

    _dictionary_cache: dict = dict()

    id: float = 0

    modelId: int = 0

    name: str = ""

    description: str = ""

    colors: list

    sex: bool = False

    level: int = 0

    ownerId: float = 0

    experience: float = 0

    experienceForLevel: float = 0

    experienceForNextLevel: float = 0

    xpRatio: int

    maxPods: int = 0

    isRideable: bool = False

    isWild: bool = False

    borning: bool = False

    energy: int = 0

    energyMax: int = 0

    stamina: int = 0

    staminaMax: int = 0

    maturity: int = 0

    maturityForAdult: int = 0

    serenity: int = 0

    serenityMax: int = 0

    aggressivityMax: int = 0

    love: int = 0

    loveMax: int = 0

    fecondationTime: int = 0

    isFecondationReady: bool

    reproductionCount: int = 0

    reproductionCountMax: int = 0

    boostLimiter: int = 0

    boostMax: float = 0

    harnessGID: int = 0

    useHarnessColors: bool

    effectList: list

    ancestor: object

    ability: list

    _model: Mount

    _familyHeadUri: str

    def __init__(self):
        self.effectList = list()
        self.ability = list()
        super().__init__()

    @classmethod
    def makeMountData(cls, o, cache=True, xpRatio=0):
        ability = 0
        nEffect = 0
        i = 0
        mountData = MountData()
        if cls._dictionary_cache.get(o.id) and cache:
            mountData = cls.getMountFromCache(o.id)

        mount = Mount.getMountById(o.model)
        mountData.name = o.name if o.name else I18n.getUiText("ui.common.noName")
        mountData.id = o.id
        mountData.modelId = o.model
        mountData.description = mount.name
        mountData.sex = o.sex
        mountData.ownerId = o.ownerId
        mountData.level = o.level
        mountData.experience = o.experience
        mountData.experienceForLevel = o.experienceForLevel
        mountData.experienceForNextLevel = o.experienceForNextLevel
        mountData.xpRatio = xpRatio

        try:
            mountData.entityLook = None
            mountData.colors = mountData.entityLook.getColors()
        except Exception as e:
            pass

        a = o.ancestor[:]
        a.insert(0, o.model)
        mountData.ancestor = cls.makeParent(a, 0, -1, 0)
        mountData.ability = []
        for ability in o.behaviors:
            mountData.ability.append(MountBehavior.getMountBehaviorById(ability))

        mountData.effectList = []
        nEffect = int(len(o.effectList))
        for i in range(nEffect):
            mountData.effectList.append(ObjectEffectAdapter.fromNetwork(o.effectList[i]))

        mountData.maxPods = o.maxPods
        mountData.isRideable = o.isRideable
        mountData.isWild = o.isWild
        mountData.energy = o.energy
        mountData.energyMax = o.energyMax
        mountData.stamina = o.stamina
        mountData.staminaMax = o.staminaMax
        mountData.maturity = o.maturity
        mountData.maturityForAdult = o.maturityForAdult
        mountData.serenity = o.serenity
        mountData.serenityMax = o.serenityMax
        mountData.aggressivityMax = o.aggressivityMax
        mountData.love = o.love
        mountData.loveMax = o.loveMax
        mountData.fecondationTime = o.fecondationTime
        mountData.isFecondationReady = o.isFecondationReady
        mountData.reproductionCount = o.reproductionCount
        mountData.reproductionCountMax = o.reproductionCountMax
        mountData.boostLimiter = o.boostLimiter
        mountData.boostMax = o.boostMax
        mountData.harnessGID = o.harnessGID
        mountData.useHarnessColors = o.useHarnessColors

        if not cls._dictionary_cache.get(o.id) or not cache:
            cls._dictionary_cache[mountData.id] = mountData

        return mountData

    @classmethod
    def getMountFromCache(cls, id: int) -> "MountData":
        return cls._dictionary_cache.get(id)

    @classmethod
    def makeParent(cls, ancestor, generation, start, index):
        nextStart = start + int(2 ** (generation - 1))
        ancestorIndex = nextStart + index
        if len(ancestor) <= ancestorIndex:
            return None

        mount = Mount.getMountById(ancestor[ancestorIndex])
        if not mount:
            return None

        return {
            "mount": mount,
            "mother": cls.makeParent(ancestor, generation + 1, nextStart, 2 * (ancestorIndex - nextStart)),
            "father": cls.makeParent(ancestor, generation + 1, nextStart, 1 + 2 * (ancestorIndex - nextStart)),
            "entityLook": None,
        }

    @property
    def model(self) -> Mount:
        if not self._model:
            self._model = Mount.getMountById(self.modelId)
        return self._model

    @property
    def familyHeadUri(self) -> str:
        family: MountFamily = None
        if not self._familyHeadUri:
            family = MountFamily.getMountFamilyById(self.model.familyId)
            self._familyHeadUri = family.headUri
        return self._familyHeadUri
