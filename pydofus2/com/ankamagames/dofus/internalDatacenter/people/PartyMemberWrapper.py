from pydofus2.com.ankamagames.dofus.network.types.game.look.EntityLook import EntityLook
from pydofus2.com.ankamagames.jerakine.interfaces.IDataCenter import IDataCenter


class PartyMemberWrapper(IDataCenter):

    id: float

    name: str

    isMember: bool

    isLeader: bool

    level: int

    breedId: int

    entityLook: EntityLook

    lifePoints: int

    maxLifePoints: int

    maxInitiative: int

    prospecting: int

    rank: int

    alignmentSide: int

    regenRate: int

    hostId: float

    hostName: str

    worldX: int = 0

    worldY: int = 0

    mapId: float = 0

    subAreaId: int = 0

    status: int = 1

    companions: list

    isInArenaParty: bool = False

    def __init__(
        self,
        id: float,
        name: str,
        status: int,
        isMember: bool,
        isLeader: bool = False,
        level: int = 0,
        entityLook: EntityLook = None,
        lifePoints: int = 0,
        maxLifePoints: int = 0,
        maxInitiative: int = 0,
        prospecting: int = 0,
        alignmentSide: int = 0,
        regenRate: int = 0,
        rank: int = 0,
        worldX: int = 0,
        worldY: int = 0,
        mapId: float = 0,
        subAreaId: int = 0,
        breedId: int = 0,
        companions: list = None,
    ):
        self.companions = list()
        super().__init__()
        self.id = id
        self.name = name
        self.isMember = isMember
        self.isLeader = isLeader
        self.level = level
        self.entityLook = entityLook
        self.breedId = breedId
        self.lifePoints = lifePoints
        self.maxLifePoints = maxLifePoints
        self.maxInitiative = maxInitiative
        self.prospecting = prospecting
        self.alignmentSide = alignmentSide
        self.regenRate = regenRate
        self.rank = rank
        self.worldX = worldX
        self.worldY = worldY
        self.mapId = mapId
        self.subAreaId = subAreaId
        self.status = status
        if not companions:
            self.companions = list()
        else:
            self.companions = companions

    @property
    def initiative(self) -> int:
        return self.maxInitiative * self.lifePoints / self.maxLifePoints
