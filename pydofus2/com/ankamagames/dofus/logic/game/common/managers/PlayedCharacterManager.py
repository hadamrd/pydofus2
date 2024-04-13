import threading
from typing import TYPE_CHECKING

from pydofus2.com.ankamagames.dofus.datacenter.jobs.Job import Job
from pydofus2.com.ankamagames.dofus.datacenter.world.MapPosition import MapPosition
from pydofus2.com.ankamagames.dofus.internalDatacenter.mount.MountData import MountData
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.DofusEntities import DofusEntities
from pydofus2.com.ankamagames.dofus.misc.utils.CharacterIdConverter import CharacterIdConverter
from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.Vertex import Vertex

if TYPE_CHECKING:
    from pydofus2.com.ankamagames.dofus.network.types.game.character.choice.CharacterBaseInformations import (
        CharacterBaseInformations,
    )
    from pydofus2.com.ankamagames.dofus.internalDatacenter.stats.EntityStats import EntityStats
    from pydofus2.com.ankamagames.dofus.datacenter.world.SubArea import SubArea
    from pydofus2.com.ankamagames.dofus.datacenter.world.WorldMap import WorldMap
    from pydofus2.com.ankamagames.dofus.internalDatacenter.jobs.KnownJobWrapper import (
        KnownJobWrapper,
    )
    from pydofus2.com.ankamagames.dofus.internalDatacenter.world.WorldPointWrapper import (
        WorldPointWrapper,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.character.characteristic.CharacterCharacteristicsInformations import (
        CharacterCharacteristicsInformations,
    )
    from pydofus2.com.ankamagames.dofus.network.types.game.look.EntityLook import EntityLook
    from pydofus2.com.ankamagames.dofus.network.types.game.character.restriction.ActorRestrictionsInformations import (
        ActorRestrictionsInformations,
    )
    from pydofus2.com.ankamagames.atouin.data.map.Cell import Cell
    from pydofus2.com.ankamagames.dofus.internalDatacenter.spells.SpellWrapper import SpellWrapper
    from pydofus2.com.ankamagames.dofus.types.entities.AnimatedCharacter import AnimatedCharacter
    from pydofus2.com.ankamagames.dofus.internalDatacenter.items.WeaponWrapper import WeaponWrapper
    from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint

from pydofus2.com.ankamagames.dofus.internalDatacenter.DataEnum import DataEnum
from pydofus2.com.ankamagames.dofus.logic.common.managers.StatsManager import StatsManager
from pydofus2.com.ankamagames.dofus.network.enums.CharacterInventoryPositionEnum import CharacterInventoryPositionEnum
from pydofus2.com.ankamagames.dofus.network.enums.PlayerLifeStatusEnum import PlayerLifeStatusEnum
from pydofus2.com.ankamagames.dofus.network.ProtocolConstantsEnum import ProtocolConstantsEnum
from pydofus2.com.ankamagames.jerakine.interfaces.IDestroyable import IDestroyable
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton
from pydofus2.com.ankamagames.jerakine.types.Callback import Callback
from pydofus2.damageCalculation.tools.StatIds import StatIds
from pydofus2.flash.geom.Point import Point


class PlayedCharacterManager(IDestroyable, metaclass=Singleton):

    def __init__(self):
        self._followingPlayerIds = list[float]()
        self._infosAvailableCallbacks = list[Callback]()
        self.playerForgettableSpelldict = dict()
        self.lastCoord = Point(0, 0)
        self.waitingGifts = list()
        self._infos = None
        self._currentSubArea: "SubArea" = None
        self._currentMap: "WorldPointWrapper" = None
        self.previousMap: "WorldPointWrapper" = None
        self.previousSubArea: "SubArea" = None
        self.previousWorldMapId: int = 0
        self.jobs = dict[int, "KnownJobWrapper"]()
        self.isInExchange = False
        self.isInHisHouse = False
        self.isInHouse = False
        self.isIndoor = False
        self.isInHisHavenbag = False
        self.isInHavenbag = False
        self.currentHavenbagRooms = list["HavenBagRoomPreviewInformation"]()
        self.isInBreach = False
        self.isInAnomaly = False
        self.restrictions: "ActorRestrictionsInformations" = None
        self.realEntityLook: "EntityLook" = None
        self.characteristics: "CharacterCharacteristicsInformations" = None
        self.spellsInventory = list["SpellWrapper"]()
        self.playerSpellList = list["SpellWrapper"]()
        self.playerShortcutList = list()
        self.inventory = list["ItemWrapper"]()
        self.currentWeapon: "WeaponWrapper" = None
        self.inventoryWeight = 0
        self.shopWeight = 0
        self.inventoryWeightMax = 0
        self.state = 0
        self.publicMode = False
        self.isPetsMounting = False
        self.petsMount = None
        self.hasCompanion = False
        self.mount: MountData = None
        self.teamId = 0
        self.isSpectator = False
        self.experiencePercent = 0
        self.achievementPoints = 0
        self.achievementPercent = 0
        self.applicationInfo = None
        self.guildApplicationInfo = None
        self.speedAjust: int = 0
        self.isInParty: bool = False
        self.playerMaxForgettableSpellsfloat: int = -1
        self._knownZaapMapIds: list[float] = list()
        self._isPartyLeader: bool = False
        self.isFighting = False
        self.instanceId = None
        self.isRiding = False
        self.lock = threading.Lock()
        super().__init__()

    @property
    def id(self) -> float:
        if self.infos:
            return float(self.infos.id)
        return 0

    @id.setter
    def id(self, id: float) -> None:
        if self.infos:
            self.infos.id = float(id)

    @property
    def infos(self) -> "CharacterBaseInformations":
        return self._infos

    @infos.setter
    def infos(self, pInfos: "CharacterBaseInformations") -> None:
        callback: Callback = None
        self._infos = pInfos
        for callback in self._infosAvailableCallbacks:
            callback.exec()

    @property
    def currVertex(self) -> Vertex:
        from pydofus2.com.ankamagames.dofus.modules.utils.pathFinding.world.WorldGraph import WorldGraph

        if self.currentZoneRp is None or self.currentMap is None:
            return None
        v = WorldGraph().getVertex(self.currentMap.mapId, self.currentZoneRp)
        if v is None:
            potentialVerticies = WorldGraph().getVertices(PlayedCharacterManager().currentMap.mapId)
            if not potentialVerticies:
                Logger().error(f"Weird that no vertex is found for map {PlayedCharacterManager().currentMap.mapId}!")
            else:
                Logger().debug(potentialVerticies)
                for zoneId, v in potentialVerticies.items():
                    if self.currentZoneRp and zoneId == self.currentZoneRp:
                        return v
                else:
                    return potentialVerticies[1]
        else:
            return v

    @property
    def stats(self) -> "EntityStats":
        return StatsManager().getStats(self.id)

    @property
    def cantMinimize(self) -> bool:
        return self.restrictions.cantMinimize

    @property
    def forceSlowWalk(self) -> bool:
        return self.restrictions.forceSlowWalk

    @property
    def cantUseTaxCollector(self) -> bool:
        return self.restrictions.cantUseTaxCollector

    @property
    def cantTrade(self) -> bool:
        return self.restrictions.cantTrade

    @property
    def cantRun(self) -> bool:
        return self.restrictions.cantRun

    @property
    def cantMove(self) -> bool:
        return self.restrictions.cantMove

    @property
    def cantBeChallenged(self) -> bool:
        return self.restrictions.cantBeChallenged

    @property
    def cantBeAttackedByMutant(self) -> bool:
        return self.restrictions.cantBeAttackedByMutant

    @property
    def cantBeAggressed(self) -> bool:
        return self.restrictions.cantBeAggressed

    @property
    def cantAttack(self) -> bool:
        return self.restrictions.cantAttack

    @property
    def cantAgress(self) -> bool:
        return self.restrictions.cantAggress

    @property
    def cantChallenge(self) -> bool:
        return self.restrictions.cantChallenge

    @property
    def cantExchange(self) -> bool:
        return self.restrictions.cantExchange

    @property
    def cantChat(self) -> bool:
        return self.restrictions.cantChat

    @property
    def cantBeMerchant(self) -> bool:
        return self.restrictions.cantBeMerchant

    @property
    def cantUseobject(self) -> bool:
        return self.restrictions.cantUseobject

    @property
    def cantUseInteractiveobject(self) -> bool:
        return self.restrictions.cantUseInteractive

    @property
    def cantSpeakToNpc(self) -> bool:
        return self.restrictions.cantSpeakToNPC

    @property
    def cantChangeZone(self) -> bool:
        return self.restrictions.cantChangeZone

    @property
    def cantAttackMonster(self) -> bool:
        return self.restrictions.cantAttackMonster

    @property
    def isInFight(self) -> bool:
        from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel

        return Kernel().fightContextFrame

    @property
    def isInKoli(self) -> bool:
        from pydofus2.com.ankamagames.dofus.kernel.Kernel import Kernel

        fightContextFrame = Kernel().fightContextFrame
        return fightContextFrame and fightContextFrame.isKolossium

    @property
    def limitedLevel(self) -> int:
        if self.infos:
            if self.infos.level > ProtocolConstantsEnum.MAX_LEVEL:
                return ProtocolConstantsEnum.MAX_LEVEL
            return self.infos.level
        return 0

    @property
    def currentWorldMap(self) -> "WorldMap":
        if self.currentSubArea:
            return self.currentSubArea.worldmap
        return None

    @property
    def currentMap(self) -> "WorldPointWrapper":
        return self._currentMap

    @property
    def currentSubArea(self) -> "SubArea":
        return self._currentSubArea

    @property
    def currentWorldMapId(self) -> int:
        if self.currentSubArea and self.currentSubArea.worldmap:
            return self.currentSubArea.worldmap.id
        return -1

    @property
    def entity(self) -> "AnimatedCharacter":
        return DofusEntities().getEntity(self.id)

    @property
    def playerMapPoint(self) -> "MapPoint":
        if self.entity is None:
            Logger().error("Can't get current MapPoint for reason : player entity not found!")
            return None
        return self.entity.position

    @property
    def currentCellId(self) -> int:
        if self.playerMapPoint is None:
            return None
        return self.playerMapPoint.cellId

    @property
    def isMutated(self) -> bool:
        from pydofus2.com.ankamagames.dofus.logic.game.common.managers.InventoryManager import InventoryManager

        rpBuffs = InventoryManager().inventory.getView("roleplayBuff").content
        if rpBuffs:
            for buff in rpBuffs:
                if (
                    buff
                    and buff.typeId == DataEnum.ITEM_TYPE_MUTATIONS
                    and buff.position == CharacterInventoryPositionEnum.INVENTORY_POSITION_MUTATION
                ):
                    return True
        return False

    @property
    def isPartyLeader(self) -> bool:
        return self._isPartyLeader

    @isPartyLeader.setter
    def isPartyLeader(self, b: bool) -> None:
        if not self.isInParty:
            self._isPartyLeader = False
        else:
            self._isPartyLeader = b

    @property
    def isGhost(self) -> bool:
        return self.state == PlayerLifeStatusEnum.STATUS_PHANTOM

    @property
    def artworkId(self) -> int:
        return (
            self.infos.entityLook.bonesId == int(self.infos.entityLook.skins[0])
            if 1
            else int(self.infos.entityLook.bonesId)
        )

    @property
    def followingPlayerIds(self) -> list[float]:
        return self._followingPlayerIds

    @currentMap.setter
    def currentMap(self, map: "WorldPointWrapper") -> None:
        if self._currentMap:
            if map.mapId != self._currentMap.mapId:
                self.previousMap = self._currentMap
                self._currentMap = map
            elif not self.isInHavenbag:
                self._currentMap.setOutdoorCoords(map.outdoorX, map.outdoorY)
            else:
                self._currentMap.setOutdoorCoords(self.previousMap.outdoorX, self.previousMap.outdoorY)
        else:
            self._currentMap = map

    @property
    def currMapPos(self) -> "MapPosition":
        return MapPosition.getMapPositionById(self.currentMap.mapId)

    @currentSubArea.setter
    def currentSubArea(self, area: "SubArea") -> None:
        if not self._currentSubArea or area != self._currentSubArea:
            if self.currentSubArea and self.currentSubArea.worldmap:
                self.previousWorldMapId = self._currentSubArea.worldmap.id
                self.previousSubArea = self.currentSubArea
            self._currentSubArea = area

    @followingPlayerIds.setter
    def followingPlayerIds(self, pPlayerIds: list[float]) -> None:
        self._followingPlayerIds = pPlayerIds

    @property
    def canBeAggressedByMonsters(self) -> bool:
        stats: "EntityStats" = StatsManager().getStats(self.id)
        if stats == None:
            return True
        if stats.getStatTotalValue(StatIds.ENERGY_POINTS) == 0:
            return False
        return not self.restrictions.cantAttackMonster

    def levelDiff(self, targetLevel: int) -> int:
        diff: int = 0
        playerLevel: int = self.limitedLevel
        if targetLevel > ProtocolConstantsEnum.MAX_LEVEL:
            targetLevel = ProtocolConstantsEnum.MAX_LEVEL
        type: int = 1
        if targetLevel < playerLevel:
            type = -1
        if abs(targetLevel - playerLevel) > 20:
            diff = 1 * type
        elif targetLevel > playerLevel:
            if targetLevel / playerLevel < 1.2:
                diff = 0
            else:
                diff = 1 * type
        elif playerLevel / targetLevel < 1.2:
            diff = 0
        else:
            diff = 1 * type
        return diff

    @property
    def currentCell(self) -> "Cell":
        from pydofus2.com.ankamagames.atouin.managers.MapDisplayManager import MapDisplayManager

        if self.currentCellId is None:
            return None
        if MapDisplayManager().dataMap is None:
            return None
        return MapDisplayManager().dataMap.cells[self.currentCellId]

    @property
    def currentZoneRp(self) -> int:
        if self.currentCell is None:
            return None
        return self.currentCell.linkedZoneRP

    @property
    def name(self) -> str:
        if self.infos:
            return self.infos.name
        return None

    @property
    def extractedServerCharacterIdFromInterserverCharacterId(self) -> int:
        return CharacterIdConverter.extractServerCharacterIdFromInterserverCharacterId(self.id)

    def addInfosAvailableCallback(self, pCallback: Callback) -> None:
        self._infosAvailableCallbacks.append(pCallback)

    def jobsLevel(self) -> int:
        job: "KnownJobWrapper" = None
        jobsLevel: int = 0
        for job in self.jobs.values():
            jobsLevel += job.jobLevel
        return jobsLevel

    def distanceFromCell(self, mp) -> int:
        return self.entity.position.distanceToCell(mp)

    def joblevel(self, jobId) -> int:
        if jobId not in self.jobs:
            if jobId != 1:  # base
                job = Job.getJobById(jobId)
                Logger().warn(f"Job '{job.name}' not in player Jobs : {self.jobs}")
            return -1
        return self.jobs[jobId].jobLevel

    def jobsfloat(self, onlyLevelOne: bool = False) -> int:
        job: "KnownJobWrapper" = None
        length: int = 0
        for job in self.jobs.values():
            if not (job.jobLevel != 1 and onlyLevelOne):
                length += 1
        return length

    def updateKnownZaaps(self, knownZaapMapIds: list[float]) -> None:
        self._knownZaapMapIds = knownZaapMapIds

    def isZaapKnown(self, mapId: float) -> bool:
        if not self._knownZaapMapIds:
            return False
        return mapId in self._knownZaapMapIds

    def jobsNumber(self, onlyLevelOne: bool = False) -> int:
        length: int = 0
        for job in self.jobs.values():
            if not (job.jobLevel != 1 and onlyLevelOne):
                length += 1
        return length

    def getSpellById(self, spellId: int) -> "SpellWrapper":
        for spellw in self.playerSpellList:
            if spellw.id == spellId:
                return spellw

    def inSameRpZone(self, cellId: int) -> bool:
        from pydofus2.com.ankamagames.atouin.managers.MapDisplayManager import MapDisplayManager

        tgtRpZone = MapDisplayManager().dataMap.cells[cellId].linkedZoneRP
        return tgtRpZone == self.currentZoneRp

    def isDead(self) -> bool:
        return PlayerLifeStatusEnum(self.state) != PlayerLifeStatusEnum.STATUS_ALIVE_AND_KICKING

    def isPodsFull(self, pourcent=0.95):
        return (
            PlayedCharacterManager().inventoryWeightMax > 0
            and PlayedCharacterManager().inventoryWeight / PlayedCharacterManager().inventoryWeightMax > pourcent
        )
