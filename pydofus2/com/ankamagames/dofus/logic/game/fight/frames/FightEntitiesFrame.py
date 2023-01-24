from typing import TYPE_CHECKING

import pydofus2.com.ankamagames.dofus.kernel.Kernel as krnl
import pydofus2.com.ankamagames.dofus.logic.game.common.managers.PlayedCharacterManager as pcm
from pydofus2.com.ankamagames.atouin.managers.MapDisplayManager import MapDisplayManager
from pydofus2.com.ankamagames.dofus.internalDatacenter.world.WorldPointWrapper import WorldPointWrapper
from pydofus2.com.ankamagames.dofus.logic.common.managers.PlayerManager import PlayerManager
from pydofus2.com.ankamagames.dofus.logic.common.managers.StatsManager import StatsManager
from pydofus2.com.ankamagames.dofus.logic.game.common.frames.AbstractEntitiesFrame import AbstractEntitiesFrame
from pydofus2.com.ankamagames.dofus.logic.game.common.misc.DofusEntities import DofusEntities
from pydofus2.com.ankamagames.dofus.logic.game.fight.actions.RemoveEntityAction import RemoveEntityAction

if TYPE_CHECKING:
    pass

from pydofus2.com.ankamagames.dofus.logic.game.fight.managers.CurrentPlayedFighterManager import CurrentPlayedFighterManager
from pydofus2.com.ankamagames.dofus.logic.game.fight.miscs.FightEntitiesHolder import FightEntitiesHolder
from pydofus2.com.ankamagames.dofus.network.enums.GameActionFightInvisibilityStateEnum import (
    GameActionFightInvisibilityStateEnum,
)
from pydofus2.com.ankamagames.dofus.network.enums.TeamEnum import TeamEnum
from pydofus2.com.ankamagames.dofus.network.messages.game.actions.fight.GameActionFightCarryCharacterMessage import (
    GameActionFightCarryCharacterMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.actions.fight.GameActionFightDropCharacterMessage import (
    GameActionFightDropCharacterMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.actions.fight.GameActionFightThrowCharacterMessage import (
    GameActionFightThrowCharacterMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.character.status.PlayerStatusUpdateMessage import (
    PlayerStatusUpdateMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.character.GameFightRefreshFighterMessage import (
    GameFightRefreshFighterMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.character.GameFightShowFighterMessage import (
    GameFightShowFighterMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.character.GameFightShowFighterRandomStaticPoseMessage import (
    GameFightShowFighterRandomStaticPoseMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightHumanReadyStateMessage import (
    GameFightHumanReadyStateMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.fight.GameFightPlacementSwapPositionsMessage import (
    GameFightPlacementSwapPositionsMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameContextRefreshEntityLookMessage import (
    GameContextRefreshEntityLookMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameEntitiesDispositionMessage import (
    GameEntitiesDispositionMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.GameEntityDispositionMessage import (
    GameEntityDispositionMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.anomaly.AnomalyStateMessage import (
    AnomalyStateMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.breach.MapComplementaryInformationsBreachMessage import (
    MapComplementaryInformationsBreachMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.MapComplementaryInformationsDataInHouseMessage import (
    MapComplementaryInformationsDataInHouseMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.MapComplementaryInformationsDataMessage import (
    MapComplementaryInformationsDataMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.MapComplementaryInformationsWithCoordsMessage import (
    MapComplementaryInformationsWithCoordsMessage,
)
from pydofus2.com.ankamagames.dofus.network.messages.game.context.roleplay.MapRewardRateMessage import MapRewardRateMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.ShowCellMessage import ShowCellMessage
from pydofus2.com.ankamagames.dofus.network.messages.game.context.ShowCellSpectatorMessage import ShowCellSpectatorMessage
from pydofus2.com.ankamagames.dofus.network.types.game.context.EntityDispositionInformations import (
    EntityDispositionInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightCharacterInformations import (
    GameFightCharacterInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightEntityInformation import (
    GameFightEntityInformation,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterInformations import (
    GameFightFighterInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightFighterNamedInformations import (
    GameFightFighterNamedInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.fight.GameFightMonsterInformations import (
    GameFightMonsterInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.FightEntityDispositionInformations import (
    FightEntityDispositionInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.context.GameContextActorInformations import GameContextActorInformations
from pydofus2.com.ankamagames.dofus.network.types.game.context.GameContextActorPositionInformations import (
    GameContextActorPositionInformations,
)
from pydofus2.com.ankamagames.dofus.network.types.game.interactive.InteractiveElement import InteractiveElement
from pydofus2.com.ankamagames.dofus.network.types.game.interactive.StatedElement import StatedElement
from pydofus2.com.ankamagames.dofus.network.types.game.look.EntityLook import EntityLook
from pydofus2.com.ankamagames.dofus.types.entities.AnimatedCharacter import AnimatedCharacter
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.messages.Frame import Frame
from pydofus2.com.ankamagames.jerakine.messages.Message import Message
from pydofus2.com.ankamagames.jerakine.types.positions.MapPoint import MapPoint
from pydofus2.damageCalculation.tools.StatIds import StatIds

logger = Logger("Dofus2")


class FightEntitiesFrame(AbstractEntitiesFrame, Frame):

    TEAM_CIRCLE_COLOR_1: int = 255

    TEAM_CIRCLE_COLOR_2: int = 16711680

    _ie: dict

    _tempFighterList: list[GameContextActorInformations] = []

    _illusionEntities: dict

    _lastKnownPosition: dict

    _lastKnownMovementPoint: dict

    _lastKnownPlayerStatus: dict

    _realFightersLooks: dict = {}

    _mountsVisible: bool

    _numCreatureSwitchingEntities: int

    _entitiesIconsToUpdate: list[float]

    lastKilledChallengers: list[GameFightFighterInformations]

    lastKilledDefenders: list[GameFightFighterInformations]

    def __init__(self):
        self._ie = dict()
        self._tempFighterList = []
        self._entitiesIconsToUpdate = list[float]()
        self.lastKilledChallengers = list[GameFightFighterInformations]()
        self.lastKilledDefenders = list[GameFightFighterInformations]()
        super().__init__()

    @classmethod
    def getCurrentInstance(cls) -> "FightEntitiesFrame":
        return krnl.Kernel().worker.getFrame("FightEntitiesFrame")

    def pushed(self) -> bool:
        self._illusionEntities = dict()
        self._lastKnownPosition = dict()
        self._lastKnownMovementPoint = dict()
        self._lastKnownPlayerStatus = dict()
        self._realFightersLooks = dict()
        return super().pushed()

    def addLastKilledAlly(self, entity: GameFightFighterInformations) -> None:
        listKilled: list[GameFightFighterInformations] = (
            self.lastKilledChallengers
            if entity.spawnInfo.teamId == TeamEnum.TEAM_CHALLENGER
            else self.lastKilledDefenders
        )
        index: int = 0
        if not isinstance(entity, GameFightFighterNamedInformations):
            while index < len(listKilled) and isinstance(listKilled[index], GameFightFighterNamedInformations):
                index += 1
            if not isinstance(entity, GameFightEntityInformation):
                while index < len(listKilled) and isinstance(listKilled[index], GameFightEntityInformation):
                    index += 1
        if entity.spawnInfo.teamId == TeamEnum.TEAM_CHALLENGER:
            self.lastKilledChallengers.insert(index, entity)
        else:
            self.lastKilledDefenders.insert(index, entity)

    def removeSpecificKilledAlly(self, infos: GameFightFighterInformations) -> None:
        if infos.spawnInfo.teamId == TeamEnum.TEAM_CHALLENGER and len(self.lastKilledChallengers) > 0:
            self.lastKilledChallengers.pop(self.lastKilledChallengers.index(infos))
        elif infos.spawnInfo.teamId == TeamEnum.TEAM_DEFENDER and len(self.lastKilledDefenders) > 0:
            self.lastKilledDefenders.pop(self.lastKilledDefenders.index(infos))

    def removeLastKilledAlly(self, teamId: int) -> None:
        if teamId == TeamEnum.TEAM_CHALLENGER and len(self.lastKilledChallengers) > 0:
            self.lastKilledChallengers.pop(0)
        elif teamId == TeamEnum.TEAM_DEFENDER and len(self.lastKilledDefenders) > 0:
            self.lastKilledDefenders.pop(0)

    def addOrUpdateActor(self, infos: GameContextActorInformations) -> AnimatedCharacter:
        res = super().addOrUpdateActor(infos)
        if infos.disposition.cellId != -1:
            self.setLastKnownEntityPosition(infos.contextualId, infos.disposition.cellId)
        if infos.contextualId > 0:
            pass
        if CurrentPlayedFighterManager().currentFighterId == infos.contextualId:
            res.canSeeThrough = True
        if isinstance(infos, GameFightCharacterInformations):
            self._lastKnownPlayerStatus[infos.contextualId] = infos.status.statusId
        return res

    def process(self, msg: Message) -> bool:

        if isinstance(msg, GameFightRefreshFighterMessage):
            gfrfmsg = msg
            actorId = gfrfmsg.informations.contextualId
            fullInfos = self._entities.get(actorId)
            if fullInfos != None:
                fullInfos.disposition = gfrfmsg.informations.disposition
                fullInfos.look = gfrfmsg.informations.look
                self._realFightersLooks[gfrfmsg.informations.contextualId] = gfrfmsg.informations.look
                if (
                    krnl.Kernel().worker.contains(fightPreparationFrame.FightPreparationFrame)
                    and gfrfmsg.informations.disposition.cellId == -1
                ):
                    self.registerActor(gfrfmsg.informations)
                else:
                    self.updateActor(fullInfos, True)
            if krnl.Kernel().worker.getFrame("FightPreparationFrame"):
                pass
            return True

        if isinstance(msg, GameFightShowFighterMessage):
            gfsfmsg = msg
            self._realFightersLooks[gfsfmsg.informations.contextualId] = gfsfmsg.informations.look
            if isinstance(msg, GameFightShowFighterRandomStaticPoseMessage):
                self.updateFighter(gfsfmsg.informations)
                self._illusionEntities[gfsfmsg.informations.contextualId] = True
            else:
                self.addOrUpdateActor(gfsfmsg.informations)
                self._illusionEntities[gfsfmsg.informations.contextualId] = False
            return False

        if isinstance(msg, GameFightHumanReadyStateMessage):
            gfhrsmsg = msg
            fighterInfoToBeReady = self.getEntityInfos(gfhrsmsg.characterId)
            if not fighterInfoToBeReady or fighterInfoToBeReady.disposition.cellId == -1:
                return True
            self.addOrUpdateActor(fighterInfoToBeReady)
            if gfhrsmsg.isReady:
                pass
            else:
                if gfhrsmsg.characterId == pcm.PlayedCharacterManager().id:
                    pass
            fightPreparationFrame = krnl.Kernel().worker.getFrame("FightPreparationFrame")
            if fightPreparationFrame:
                pass
            return True

        if isinstance(msg, GameEntityDispositionMessage):
            gedmsg = msg
            if gedmsg.disposition.id == CurrentPlayedFighterManager().currentFighterId:
                pass
            self.updateActorDisposition(gedmsg.disposition.id, gedmsg.disposition)
            return True

        if isinstance(msg, GameFightPlacementSwapPositionsMessage):
            gfpspmsg = msg
            for iedi in gfpspmsg.dispositions:
                self.updateActorDisposition(iedi.id, iedi)
            return True

        if isinstance(msg, GameEntitiesDispositionMessage):
            gedsmsg = msg
            for disposition in gedsmsg.dispositions:
                fighterInfos = self.getEntityInfos(disposition.id)
                if (
                    fighterInfos
                    and fighterInfos.stats.invisibilityState != GameActionFightInvisibilityStateEnum.INVISIBLE
                ):
                    self.updateActorDisposition(disposition.id, disposition)
            return True

        if isinstance(msg, GameContextRefreshEntityLookMessage):
            return True

        if isinstance(msg, RemoveEntityAction):
            fighterRemovedId = msg.actorId
            self.removeActor(fighterRemovedId)
            del self._realFightersLooks[fighterRemovedId]
            return True

        if isinstance(msg, ShowCellSpectatorMessage):
            return True

        if isinstance(msg, ShowCellMessage):
            return True

        if isinstance(msg, MapComplementaryInformationsDataMessage):
            mcidmsg = msg
            self._interactiveElements = mcidmsg.interactiveElements
            if isinstance(msg, MapComplementaryInformationsWithCoordsMessage):
                mciwcmsg = msg
                if pcm.PlayedCharacterManager().isInHouse:
                    pass
                pcm.PlayedCharacterManager().isInHouse = False
                pcm.PlayedCharacterManager().isInHisHouse = False
                pcm.PlayedCharacterManager().currentMap.setOutdoorCoords(mciwcmsg.worldX, mciwcmsg.worldY)
                self._worldPoint = WorldPointWrapper(mciwcmsg.mapId, True, mciwcmsg.worldX, mciwcmsg.worldY)

            elif isinstance(msg, MapComplementaryInformationsDataInHouseMessage):
                mcidihmsg = msg
                isPlayerHouse = PlayerManager().nickname == mcidihmsg.currentHouse.houseInfos.ownerTag.nickname
                pcm.PlayedCharacterManager().isInHouse = True
                if isPlayerHouse:
                    pcm.PlayedCharacterManager().isInHisHouse = True
                pcm.PlayedCharacterManager().currentMap.setOutdoorCoords(
                    mcidihmsg.currentHouse.worldX, mcidihmsg.currentHouse.worldY
                )
                self._worldPoint = WorldPointWrapper(
                    mcidihmsg.mapId,
                    True,
                    mcidihmsg.currentHouse.worldX,
                    mcidihmsg.currentHouse.worldY,
                )

            elif isinstance(msg, MapComplementaryInformationsBreachMessage):
                return True

        if isinstance(msg, AnomalyStateMessage):
            return True

        if isinstance(msg, MapRewardRateMessage):
            return True

        if isinstance(msg, GameActionFightCarryCharacterMessage):
            gafccmsg = msg
            if gafccmsg.cellId != -1:
                for ent in self._entities:
                    if ent.contextualId == gafccmsg.targetId:
                        ent.disposition.carryingCharacterId = gafccmsg.sourceId
                        self._tempFighterList.append(TmpFighterInfos(ent.contextualId, gafccmsg.sourceId))
            return True

        if isinstance(msg, GameActionFightThrowCharacterMessage):
            gaftcmsg = msg
            self.dropEntity(gaftcmsg.targetId)
            return True

        if isinstance(msg, GameActionFightDropCharacterMessage):
            gafdcmsg = msg
            self.dropEntity(gafdcmsg.targetId)
            return True

        if isinstance(msg, PlayerStatusUpdateMessage):
            psum = msg
            self._lastKnownPlayerStatus[psum.playerId] = psum.status.statusId
            return False

        else:
            return False

    def dropEntity(self, targetId: float) -> None:
        index: int = 0
        ent: GameFightFighterInformations = None
        for ent in self._entities:
            if ent.contextualId == targetId:
                ent.disposition.carryingCharacterId = None
                index = self.getTmpFighterInfoIndex(ent.contextualId)
                if self._tempFighterList != None and len(self._tempFighterList) != 0 and index != -1:
                    self._tempFighterList.splice(index, 1)
                return

    def showCreaturesInFight(self, activated: bool = False) -> None:
        self._creaturesFightMode = activated
        self._justSwitchingCreaturesFightMode = True
        self._numCreatureSwitchingEntities = 0
        for ent in self._entities.values():
            self.updateFighter(ent)
        self._justSwitchingCreaturesFightMode = False
        if self._numCreatureSwitchingEntities == 0:
            self.onCreatureSwitchEnd(None)

    def entityIsIllusion(self, id: float) -> bool:
        return self._illusionEntities.get(id, False)

    def getLastKnownEntityPosition(self, id: float) -> int:
        return int(self._lastKnownPosition[id]) if id in self._lastKnownPosition else -1

    def setLastKnownEntityPosition(self, id: float, value: int) -> None:
        self._lastKnownPosition[id] = value

    def getLastKnownEntityMovementPoint(self, id: float) -> int:
        return int(self._lastKnownMovementPoint[id]) if id in self._lastKnownMovementPoint else 0

    def setLastKnownEntityMovementPoint(self, id: float, value: int, add: bool = False) -> None:
        if id not in self._lastKnownMovementPoint:
            self._lastKnownMovementPoint[id] = 0
        if not add:
            self._lastKnownMovementPoint[id] = value
        else:
            self._lastKnownMovementPoint[id] += value

    def pulled(self) -> bool:
        self._tempFighterList = None
        self._ie.clear()
        self._realFightersLooks.clear()
        return super().pulled()

    def registerInteractive(self, ie: InteractiveElement, firstSkill: int) -> None:
        if not MapDisplayManager().isIdentifiedElement(ie.elementId):
            logger.error("Unknown identified element " + str(ie.elementId) + ", unable to register it as interactive.")
            return
        found: bool = False
        for s, cie in enumerate(self.interactiveElements):
            if cie.elementId == ie.elementId:
                found = True
                self.interactiveElements[int(s)] = ie
        if not found:
            self.interactiveElements.append(ie)
        worldPos: MapPoint = MapDisplayManager().getIdentifiedElementPosition(ie.elementId)
        self._ie[ie.elementId] = {
            "element": ie,
            "position": worldPos,
            "firstSkill": firstSkill,
        }

    def updateStatedElement(self, se: StatedElement) -> None:
        if not MapDisplayManager().isIdentifiedElement(se.elementId):
            logger.error(
                "Unknown identified element "
                + str(se.elementId)
                + " unable to change its state to "
                + str(se.elementState)
                + " !"
            )
            return

    def removeInteractive(self, ie: InteractiveElement) -> None:
        del self._ie[ie.elementId]

    def getOrdonnedPreFighters(self) -> list[float]:
        entitiesIds: list[float] = self.getEntitiesIdsList()
        fighters: list[float] = list[float]()
        if not entitiesIds or len(entitiesIds) <= 1:
            return fighters
        goodGuys: list = list()
        badGuys: list = list()
        hiddenGuys: list = list()
        badInit: int = 0
        goodInit: int = 0
        for id in entitiesIds:
            entityInfo = self.getEntityInfos(id)
            if entityInfo:
                if isinstance(entityInfo, GameFightFighterNamedInformations) and entityInfo.hiddenInPrefight:
                    hiddenGuys.append(id)
                else:
                    stats = StatsManager().getStats(entityInfo.contextualId)
                    monsterGenericId = 0
                    if isinstance(entityInfo, GameFightMonsterInformations):
                        monsterGenericId = entityInfo.creatureGenericId
                    if stats:
                        initiative = stats.getStatTotalValue(StatIds.INITIATIVE)
                        lifePoints = stats.getHealthPoints()
                        maxLifePoints = stats.getMaxHealthPoints()
                        if entityInfo.spawnInfo.teamId == 0:
                            badGuys.append(
                                {
                                    "fighterId": id,
                                    "init": initiative * lifePoints / maxLifePoints,
                                    "monsterId": monsterGenericId,
                                }
                            )
                            badInit += initiative * lifePoints / maxLifePoints
                        else:
                            badGuys.append(
                                {
                                    "fighterId": id,
                                    "init": initiative * lifePoints / maxLifePoints,
                                    "monsterId": monsterGenericId,
                                }
                            )
                            goodInit += initiative * lifePoints / maxLifePoints
        badGuys.sort(key=lambda e: (e["init"], e["monsterId"], e["fighterId"]), reverse=True)
        goodGuys.sort(key=lambda e: (e["init"], e["monsterId"], e["fighterId"]), reverse=True)
        badStart = True
        if len(badGuys) == 0 or len(goodGuys) == 0 or badInit / len(badGuys) < goodInit / len(goodGuys):
            badStart = False
        length: int = max(len(badGuys), len(goodGuys))
        for i in range(length):
            if badStart:
                if i < len(badGuys):
                    fighters.append(badGuys[i]["fighterId"])
                if i < len(goodGuys):
                    fighters.append(goodGuys[i]["fighterId"])
            else:
                if i < len(goodGuys):
                    fighters.append(goodGuys[i]["fighterId"])
                if i < len(badGuys):
                    fighters.append(badGuys[i]["fighterId"])
        for e in hiddenGuys.reverse():
            fighters = fighters.insert(0, e)
        return fighters

    def updateFighter(self, fighterInfos: GameFightFighterInformations) -> None:
        lastInvisibilityStat: int = 0
        fighterId: float = fighterInfos.contextualId
        if fighterInfos.spawnInfo.alive:
            lastFighterInfo: GameFightFighterInformations = self._entities.get(fighterId)
            if lastFighterInfo:
                lastInvisibilityStat = lastFighterInfo.stats.invisibilityState
            self.addOrUpdateActor(fighterInfos)
            if (
                lastInvisibilityStat == GameActionFightInvisibilityStateEnum.INVISIBLE
                and fighterInfos.stats.invisibilityState == lastInvisibilityStat
            ):
                self.registerActor(fighterInfos)
                return
            if lastFighterInfo != fighterInfos and fighterId == CurrentPlayedFighterManager().currentFighterId:
                pass
            if (
                fighterInfos.stats.invisibilityState != GameActionFightInvisibilityStateEnum.VISIBLE
                and fighterInfos.stats.invisibilityState != lastInvisibilityStat
            ):
                pass
        else:
            self.updateActor(fighterInfos, False)
        self.updateCarriedEntities(fighterInfos)

    def isEntityAlive(self, entityId: float) -> bool:
        if not self.hasEntity(entityId):
            return False
        entityInfo: GameContextActorInformations = self.getEntityInfos(entityId)
        return isinstance(entityInfo, GameFightFighterInformations) and entityInfo.spawnInfo.alive

    def updateActor(self, actorInfos: GameContextActorInformations, alive: bool = True) -> None:
        if alive:
            self.addOrUpdateActor(actorInfos)
        else:
            self.registerActor(actorInfos)

    def updateCarriedEntities(self, fighterInfos: GameContextActorInformations) -> None:
        fighterId: float = fighterInfos.contextualId
        num: int = 0 if self._tempFighterList is None else len(self._tempFighterList)
        i: int = 0
        while i < num:
            infos = self._tempFighterList[i]
            carryingCharacterId = infos.carryingCharacterId
            if fighterId == carryingCharacterId:
                del self._tempFighterList[i]
            i += 1
        if isinstance(fighterInfos.disposition, FightEntityDispositionInformations):
            fedi = fighterInfos.disposition
            if fedi.carryingCharacterId:
                carryingEntity = DofusEntities.getEntity(fedi.carryingCharacterId)
                if not carryingEntity:
                    self._tempFighterList.append(TmpFighterInfos(fighterInfos.contextualId, fedi.carryingCharacterId))

    @property
    def dematerialization(self) -> bool:
        return self._creaturesFightMode

    @property
    def lastKnownPlayerStatus(self) -> dict:
        return self._lastKnownPlayerStatus

    def getRealFighterLook(self, pFighterId: float) -> EntityLook:
        return self._realFightersLooks[pFighterId]

    def setRealFighterLook(self, pFighterId: float, pEntityLook: EntityLook) -> None:
        self._realFightersLooks[pFighterId] = pEntityLook

    @property
    def charactersMountsVisible(self) -> bool:
        return self._mountsVisible

    def getEntityTeamId(self, entityId: float) -> float:
        if (entityId not in self._entities) or not isinstance(self._entities[entityId], GameFightFighterInformations):
            return -1
        entitiesInfo: GameContextActorPositionInformations = self._entities[entityId]
        if not isinstance(entitiesInfo, GameFightFighterInformations):
            return -1
        return entitiesInfo.spawnInfo.teamId

    def getEntityIdsWithTeamId(self, teamId: float) -> list[float]:
        entityIds: list[float] = list[float]()
        if teamId < 0:
            return entityIds
        for entityInfo in self._entities.values():
            if entityInfo is not None and entityInfo.spawnInfo.teamId == teamId:
                entityIds.append(entityInfo.contextualId)
        return entityIds

    def updateActorDisposition(self, actorId: float, newDisposition: EntityDispositionInformations) -> None:
        super().updateActorDisposition(actorId, newDisposition)
        if newDisposition.cellId == -1:
            actor = DofusEntities.getEntity(actorId)
            if actor:
                FightEntitiesHolder().holdEntity(actor)
        else:
            FightEntitiesHolder().unholdEntity(actorId)

    def getTmpFighterInfoIndex(self, pId: float) -> float:
        infos: TmpFighterInfos = None
        for infos in self._tempFighterList:
            if infos.contextualId == pId:
                return -1 if infos not in self._tempFighterList else self._tempFighterList.index(infos)
        return -1


class TmpFighterInfos:

    contextualId: float

    carryingCharacterId: float

    def __init__(self, pId: float, pCarryindId: float):
        super().__init__()
        self.contextualId = pId
        self.carryingCharacterId = pCarryindId
